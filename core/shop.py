import random

from data.plugins.astrbot_plugin_douniuniu.core.data_manager import DataManager
from data.plugins.astrbot_plugin_douniuniu.core.utils import probabilistic_decision, get_add_text


class Shop:
    def __init__(self):
        self.data_manager = DataManager()

        self.max_len = 5
        self.exchange_realm = 0.2
        self.viagra_times = 3
        self.items = {
            1: {"name": "伟哥", "price": 80, "description": f"无视冷却连续打胶/自摸{self.viagra_times}次"},
            2: {"name": "迷幻菌子", "price": 150,
                "description": "使用后全群陷入迷幻，立即消耗本群5个人的打胶/自摸机会为自己打胶/自摸"},
            3: {"name": "春天的药", "price": 150, "description": "使用后变得欲求不满，随机挑选5人为自己锁牛牛/吸猫猫"},
            4: {"name": "黑店壮丁手术体验卡", "price": 100,
                "description": "获得一次乡下黑店的牛牛手术机会，30%概率长度翻倍，70%概率长度减半"},
            5: {"name": "诊所壮丁手术体验卡", "price": 200,
                "description": "获得一次小镇诊所的牛牛手术机会，50%概率长度翻倍，50%概率长度减半"},
            6: {"name": "医院壮丁手术体验卡", "price": 400,
                "description": "获得一次正规医院的牛牛手术机会，70%概率长度翻倍，30%概率长度减半"},
            7: {"name": "六味地黄丸", "price": 100, "description": "下次由你主动发起的比划必胜"},
            8: {"name": "负重沙袋", "price": 100,
                "description": "一个可以使用24h，能给牛牛增加负重的道具，期间锻炼效率翻倍"},
            9: {"name": "会跳的蛋", "price": 100,
                "description": "一个可以使用24h，能给猫猫增加负担的道具，期间锻炼效率翻倍"},
            10: {"name": "性转针筒", "price": 100,
                 "description": "一针下去24h内牛牛将暂时缩腹为猫，期间打工金币翻倍，再次使用将变回牛牛"},
            11: {"name": "牛牛转换器", "price": 500,
                 "description": "可以交换评分和自己相差不超过20%的目标用户的牛牛属性"},
            12: {"name": "猫猫转换器", "price": 500,
                 "description": "可以交换评分和自己相差不超过20%的目标用户的猫猫属性"},
            13: {"name": "春风精灵", "price": 50,
                 "description": "1小时内每次冷却完毕自动打胶/自摸，输入“/春风精灵提醒 开/关”设置是否提醒"},
            14: {"name": "牛牛盲盒", "price": 150, "description": "随机获得一件商品或金币奖励"},
            15: {"name": "牛牛寄生虫", "price": 200,
                 "description": "24小时内目标用户牛牛增长的长度会被你窃取，对方寄生虫越多窃取越少"},
            16: {"name": "改名卡", "price": 50, "description": "修改牛牛的名字，名字需要在5个字以内"},
            17: {"name": "商店8折优惠券", "price": 100, "description": "使用后接下来5分钟商店所有商品将对你打8折"},
            18: {"name": "杀虫剂", "price": 50, "description": "使用后去掉一只牛牛寄生虫"},
        }

    def get_items(self, user_id) -> str:
        """获取所有商品的打印信息"""
        text = "🏬 牛牛商城 🏪\n"
        for key, value in self.items.items():
            text += f"🛒 {key}. {value['name']} 💰️ {value['price']}\n"
            text += f"     {value['description']}\n"
        money = self.data_manager.get_user_data(user_id)['coins']
        text += f'👛 持有金币：{money}\n'
        text += '发送“/购买 编号 数量”购买对应道具，不填数量将默认买1个'
        return text

    def purchase(self, user_id, item_id, num) -> str:
        if item_id > len(self.items) or item_id < 1:
            return f'✅ 商品编号错误，编号范围在1~{len(self.items)}'

        user_data = self.data_manager.get_user_data(user_id)
        user_money = user_data['coins']
        need_money = self.items[item_id]['price'] * num
        if user_money < need_money:
            return f'❌ 当前持有金币：{user_money}，需要{need_money}金币才能购买{num}个{self.items[item_id]["name"]}'

        user_data['coins'] -= num * self.items[item_id]['price']
        user_data['items_num'][self.items[item_id]['name']] += num
        now_money = user_data['coins']
        self.data_manager.save_user_data(user_id, user_data)
        return f'✅ 成功消耗{need_money}金币购买{num}个{self.items[item_id]["name"]}\n👛 剩余金币：{now_money}'

    def use_rename_card(self, user_id, name: str, config: dict) -> str:
        """使用改名卡逻辑"""
        # 名称长度判断
        if len(name) > self.max_len:
            return f"❌ 名称需要在{self.max_len}个字之内"
        user_data = self.data_manager.get_user_data(user_id)
        # 改名卡判断
        if user_data['items_num']['改名卡'] < 1:
            return "❌ 改名需要改名卡，可以在牛牛商城购买"
        # 敏感词判断
        for item in config['disabled_name']:
            if item in name:
                return "😊 这个名字不文明哦~换一个吧"
        # 成功使用
        if self.data_manager.set_niuniu_name(user_id, name):
            # 更新一下修改名字后的data
            user_data = self.data_manager.get_user_data(user_id)
            user_data['items_num']['改名卡'] -= 1
            self.data_manager.save_user_data(user_id, user_data)
            return f"✅ 成功消耗改名卡，将牛牛改名为 {name}"
        else:
            return f"❌ 你的牛牛名称已是 {name}"

    def use_drone(self, user1_id, user2_id, num: int) -> str:
        """user1向user2使用寄生虫"""
        text = ''
        user1_data = self.data_manager.get_user_data(user1_id)
        if user1_data['items_num']['牛牛寄生虫'] < num:
            text += f"❌ 你的“牛牛寄生虫”不足{num}个，输入“/牛牛商城”查看购买\n"
            return text
        user2_data = self.data_manager.get_user_data(user2_id)
        user2_niuniu_name = user2_data['niuniu_name']
        drone_num = self.data_manager.add_drone(user1_id, user2_id, num)
        text += f"🐛 寄生成功，{user2_niuniu_name}身上有{drone_num}个你投放的寄生虫\n"
        return text

    def use_insecticide(self, user_id, num: int) -> str:
        """user移除身上的第一个寄生虫"""
        text = ''
        user_data = self.data_manager.get_user_data(user_id)
        exist_drone = user_data['items']['drone']
        niuniu_name = user_data['niuniu_name']
        # 无寄生虫
        if len(exist_drone) == 0:
            text += f"❌ {niuniu_name}非常健康，身上没有寄生虫\n"
            return text
        # 杀虫剂不足
        if user_data['items_num']['杀虫剂'] < num:
            text += f"❌ 你的“杀虫剂”不足{num}个，输入“/牛牛商城”查看购买\n"
            return text
        # 各种数量对应的回复
        if num > len(exist_drone):
            text += f"❌ 使用失败，传入数字大于当前寄生虫数量：{len(exist_drone)}\n"
        elif num == len(exist_drone):
            self.data_manager.remove_drone(user_id, num)
            text += f"✅ 使用成功，杀死了全部寄生虫\n"
        elif num > 0:
            num = len(exist_drone)
            self.data_manager.remove_drone(user_id, num)
            text += f"✅ 使用成功，杀死了前{num}个寄生虫\n"
        else:
            text += f"❌ 使用失败，传入数字小于0\n"
        return text

    def use_sure_win(self, user_id):
        """使用六味地黄丸必胜"""
        text = ''
        user_data = self.data_manager.get_user_data(user_id)
        if user_data['items_num']['六味地黄丸'] < 1:
            text += f"❌ 你没有“六味地黄丸”，输入“/牛牛商城”查看购买\n"
            return text
        user_data['items_num']['六味地黄丸'] -= 1
        user_data['items']['pills'] = True
        self.data_manager.save_user_data(user_id, user_data)
        text += f"✅ 使用成功，下次由你发起的决斗必胜\n"
        return text

    def use_big_d(self, group_id, user_id, success_prob: float) -> str:
        """使用壮丁手术"""
        text = ''
        user_data = self.data_manager.get_user_data(user_id)
        if success_prob == 0.3:
            item = '黑店壮丁手术体验卡'
        elif success_prob == 0.5:
            item = '诊所壮丁手术体验卡'
        else:
            item = '医院壮丁手术体验卡'
        if user_data['items_num'][item] < 1:
            text += f"❌ 你没有“{item}”，输入“/牛牛商城”查看购买\n"
            return text
        is_add = probabilistic_decision(success_prob)
        self.data_manager.use_item(user_id, ['items_num', item])
        if is_add:
            add_length = user_data['length'] * 2
            true_add = self.data_manager.add_length(group_id, user_id, add_length)
            text += f"🏥 手术成功\n"
            text += get_add_text(true_add, add_length, user_data)
        else:
            del_length = int(user_data['length'] / 2)
            self.data_manager.del_length(user_id, del_length)
            text += f"🏥 手术失败\n"
            text += f"📏 {user_data['niuniu_name']}长度减半，当前长度：{self.data_manager.get_user_data(user_id)['length']}"
        return text

    def use_cassette(self, user_id) -> str:
        """使用牛牛盲盒"""
        # 判断是否存在道具
        user_data = self.data_manager.get_user_data(user_id)
        text = ''
        item = '牛牛盲盒'
        if user_data['items_num'][item] < 1:
            text += f"❌ 你没有“{item}”，输入“/牛牛商城”查看购买\n"
            return text
        # 使用道具
        user_data['items_num'][item] -= 1
        # 具体使用逻辑
        random_num = random.randint(1, 28)
        if random_num <= 18:
            item_name = self.items[random_num]['name']
            user_data['items_num'][item_name] += 1
            text += f'🎁 你拆开了牛牛盲盒，获得：{item_name}\n'
        else:
            coins_num = 50 * (random_num - 18)
            user_data['coins'] += coins_num
            text += f'🎁 你拆开了牛牛盲盒，获得：金币*{coins_num}\n'
        # 保存最终修改并返回文本结果
        self.data_manager.save_user_data(user_id, user_data)
        return text

    def use_exchange_niu(self,user1_id,user2_id)->str:
        """交换牛牛"""
        # 判断是否存在道具
        user1_data = self.data_manager.get_user_data(user1_id)
        text = ''
        item = '牛牛转换器'
        if user1_data['items_num'][item] < 1:
            text += f"❌ 你没有“{item}”，输入“/牛牛商城”查看购买\n"
            return text
        # 使用道具
        user1_data['items_num'][item] -= 1
        user2_data = self.data_manager.get_user_data(user2_id)
        user2_score = round(user2_data['length'] * 0.3 + user2_data['hardness'] * 0.7,2)
        user1_score = round(user1_data['length'] * 0.3 + user1_data['hardness'] * 0.7,2)
        if user1_score*(1-self.exchange_realm)<=user2_score<=user1_score*(1+self.exchange_realm):
            temp_data = user2_data.copy()
            user2_data['length'] = user1_data['length']
            user2_data['hardness'] = user1_data['hardness']
            user1_data['length'] = temp_data['length']
            user1_data['hardness'] = temp_data['hardness']
            self.data_manager.save_user_data(user1_id, user1_data)
            self.data_manager.save_user_data(user2_id, user2_data)
            # 更新排行榜
            self.data_manager.update_rank(user1_id)
            self.data_manager.update_rank(user2_id)
            text+=f"✅ 牛牛交换成功"
        else:
            text += f"❌ 交换对象的评分需要再{user1_score*(1-self.exchange_realm)}~{user1_score*(1+self.exchange_realm)}之间"
        return text

    def use_exchange_mao(self,user1_id,user2_id)->str:
        """交换猫猫"""
        # 判断是否存在道具
        user1_data = self.data_manager.get_user_data(user1_id)
        text = ''
        item = '猫猫转换器'
        if user1_data['items_num'][item] < 1:
            text += f"❌ 你没有“{item}”，输入“/牛牛商城”查看购买\n"
            return text
        # 使用道具
        user1_data['items_num'][item] -= 1
        user2_data = self.data_manager.get_user_data(user2_id)
        user2_score = round(user2_data['hole'] * 0.3 + user2_data['sensitivity'] * 0.7, 2)
        user1_score = round(user1_data['hole'] * 0.3 + user1_data['sensitivity'] * 0.7, 2)
        if user1_score*(1-self.exchange_realm)<=user2_score<=user1_score*(1+self.exchange_realm):
            temp_data = user2_data.copy()
            user2_data['hole'] = user1_data['hole']
            user2_data['sensitivity'] = user1_data['sensitivity']
            user1_data['hole'] = temp_data['hole']
            user1_data['sensitivity'] = temp_data['sensitivity']
            self.data_manager.save_user_data(user1_id, user1_data)
            self.data_manager.save_user_data(user2_id, user2_data)
            #无需更新排行榜
            text += f"✅ 猫猫交换成功"
        else:
            text += f"❌ 交换对象的评分需要再{user1_score*(1-self.exchange_realm)}~{user1_score*(1+self.exchange_realm)}之间"
        return text

    def use_viagra(self,user_id):
        """使用伟哥"""
        # 判断是否存在道具
        user_data = self.data_manager.get_user_data(user_id)
        text = ''
        item = '伟哥'
        if user_data['items_num'][item] < 1:
            text += f"❌ 你没有“{item}”，输入“/牛牛商城”查看购买\n"
            return text
        # 使用道具
        user_data['items_num'][item] -= 1
        pass

    def use_mushroom(self,user_id):
        """使用迷幻菌子"""
        # 判断是否存在道具
        user_data = self.data_manager.get_user_data(user_id)
        text = ''
        item = '迷幻菌子'
        if user_data['items_num'][item] < 1:
            text += f"❌ 你没有“{item}”，输入“/牛牛商城”查看购买\n"
            return text
        # 使用道具
        user_data['items_num'][item] -= 1
        pass

    def use_aphrodisiac(self,user_id):
        """使用春天的药"""
        # 判断是否存在道具
        user_data = self.data_manager.get_user_data(user_id)
        text = ''
        item = '春天的药'
        if user_data['items_num'][item] < 1:
            text += f"❌ 你没有“{item}”，输入“/牛牛商城”查看购买\n"
            return text
        # 使用道具
        user_data['items_num'][item] -= 1
        pass

    def use_sandbag(self,user_id):
        """使用负重沙袋"""
        # 判断是否存在道具
        user_data = self.data_manager.get_user_data(user_id)
        text = ''
        item = '负重沙袋'
        if user_data['items_num'][item] < 1:
            text += f"❌ 你没有“{item}”，输入“/牛牛商城”查看购买\n"
            return text
        # 使用道具
        user_data['items_num'][item] -= 1
        pass

    def use_jumping_egg(self,user_id):
        """使用会跳的蛋"""
        # 判断是否存在道具
        user_data = self.data_manager.get_user_data(user_id)
        text = ''
        item = '会跳的蛋'
        if user_data['items_num'][item] < 1:
            text += f"❌ 你没有“{item}”，输入“/牛牛商城”查看购买\n"
            return text
        # 使用道具
        user_data['items_num'][item] -= 1
        pass

    def use_trans(self,user_id):
        """使用性转针筒"""
        # 判断是否存在道具
        user_data = self.data_manager.get_user_data(user_id)
        text = ''
        item = '性转针筒'
        if user_data['items_num'][item] < 1:
            text += f"❌ 你没有“{item}”，输入“/牛牛商城”查看购买\n"
            return text
        # 使用道具
        user_data['items_num'][item] -= 1
        pass

    def use_fling(self,user_id):
        """使用春风精灵"""
        # 判断是否存在道具
        user_data = self.data_manager.get_user_data(user_id)
        text = ''
        item = '春风精灵'
        if user_data['items_num'][item] < 1:
            text += f"❌ 你没有“{item}”，输入“/牛牛商城”查看购买\n"
            return text
        # 使用道具
        user_data['items_num'][item] -= 1
        pass

    def use_20off(self,user_id):
        """使用八折优惠券"""
        # 判断是否存在道具
        user_data = self.data_manager.get_user_data(user_id)
        text = ''
        item = '商店8折优惠券'
        if user_data['items_num'][item] < 1:
            text += f"❌ 你没有“{item}”，输入“/牛牛商城”查看购买\n"
            return text
        # 使用道具
        user_data['items_num'][item] -= 1
