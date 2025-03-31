import random
import time

from data.plugins.astrbot_plugin_douniuniu.core.data_manager import DataManager
from data.plugins.astrbot_plugin_douniuniu.core.utils import random_normal_distribution_int, format_length, get_add_text


class DoSelf:
    def __init__(self):
        self.data_manager = DataManager()
        self.probabilities_niu = {
            '长度增加硬度减少': 35,
            '增加双属性': 30,
            '无变化': 20,  # 无变化
            '减少长度硬度不变': 10,  # 减少长度硬度不变
            '减少双属性': 5  # 减少双属性
        }
        self.reason_niu = {
            '长度增加硬度减少': [
                '😌 紧绷的牛牛耗尽了最后一丝力气完成了打胶',
                '😌 攀登上高峰的牛牛一下子就软了下来',
                '😌 打胶手法过快导致牛牛过热软化',
                '😌 成长后的牛牛失去了些年轻时的坚挺'
            ],
            '增加双属性': [
                '🥳 牛牛在打胶过程中越挫越勇，并且逐渐散发出金光',
                '🥳 牛牛似乎开始享受起了高强度打胶，并且突然开口喊你杂鱼',
                '🥳 你的牛牛秃了，也变强了',
                '🥳 你的牛牛在摩擦中变得大彻大悟，领悟了修炼硬度和长度的精髓',
                '🥳 斯巴拉西！你精湛的打胶手法让牛牛像雨后春笋般成长',
                '🥳 在你的悉心打胶下，你的牛牛成为了别人家的牛牛',
            ],
            '无变化': [
                '😑 打胶过程中牛牛脱离了你的手去追路过的猫猫',
                '😑 你的牛牛突然思考起了牛牛存在的意义，你怎么摩擦它都没反应',
                '😑 一个二次元头像的群友制止了你的打胶，你刚想反抗突然连人带牛一起被打晕',
                '😑 打胶过程中你被路过的小美吸引了注意'
            ],
            '减少长度硬度不变': [
                '😔 你的牛牛在打胶过程中不小心掉地上让人踩了一脚，踩断了一节',
                '😔 你的牛牛在打胶过程中不小心手滑飞了出去，摔断了一节',
                '😔 打胶过程中你的麒麟臂用力过猛，牛牛被你掐断了一小节',
                '😔 熟睡中的牛牛被你拉起来打胶，闹情绪的牛牛剪了自己一小节',
                '😔 一只牛牛从天而降压断了你的牛牛，事后发现这是另一个群友打胶时手滑'
            ],
            '减少双属性': [
                '😫 你的牛牛还沉浸在上次决斗失败的阴影中，打胶时自暴自弃',
                '😫 由于你打胶心切，没掌握力度和速度，牛牛在打胶过程中软化断裂',
                '😫 由于没洗手就打胶导致牛牛生病了',
                '😫 你尝试了一种很邪门的打胶手法，结果这次打胶后牛牛越来越弱'
            ]
        }

    def do_self_niu(self, group_id, user_id) -> str:
        """打胶"""
        user_data = self.data_manager.get_user_data(user_id)
        niuniu_name = user_data['niuniu_name']
        text = ''
        # 使用伟哥打胶
        if user_data['items']['viagra'] > 0:
            add_length = random_normal_distribution_int(10, 21, 1)
            true_add = self.data_manager.add_length(group_id, user_id, add_length)
            self.data_manager.use_item(user_id, ['items', 'viagra'])
            user_data = self.data_manager.get_user_data(user_id)
            remain_times = user_data['items']['viagra']
            if remain_times == 0:
                text += f'💊 伟哥次数已用完'
                # 更新打胶最后时间
                self.data_manager.set_value(user_id, ['time_recording', 'do_self'], time.time())
            else:
                text += f'💊 伟哥使用成功，剩余{remain_times}次'

            if true_add < add_length:
                text += f"📏 {niuniu_name}长度在被寄生虫蚕食后增加了{true_add}，当前长度：{format_length(user_data['length'])}\n"
                text += f'各寄生虫窃取到了{true_add}，回馈到主人的牛牛中\n'
            else:
                text += f"📏 {niuniu_name}长度增加了{true_add}，当前长度：{format_length(user_data['length'])}\n"
            return text
        # 无伟哥
        result = random.choices(
            list(self.probabilities_niu.keys()),
            weights=list(self.probabilities_niu.values()),
            k=1
        )[0]
        # 添加原因
        text += f"{random.choice(self.reason_niu[result])}\n"
        if result == '长度增加硬度减少':
            # 修改对应参数
            del_hardness = random_normal_distribution_int(1, 4, 1)
            add_length = int(del_hardness * (1 + random.random()))
            self.data_manager.del_hardness(group_id, user_id, del_hardness)
            true_add = self.data_manager.add_length(group_id, user_id, add_length)
            user_data = self.data_manager.get_user_data(user_id)
            text += get_add_text(true_add, add_length, niuniu_name, user_data)
            now_hardness = user_data['hardness']
            text += f"💪 {niuniu_name}的硬度减少{del_hardness}级，当前硬度：{now_hardness}\n"
        elif result == '增加双属性':
            add_hardness = random_normal_distribution_int(1, 4, 1)
            self.data_manager.add_hardness(group_id,user_id,add_hardness)
            add_length = random_normal_distribution_int(1, 11, 2)
            true_add = self.data_manager.add_length(group_id, user_id, add_length)
            user_data = self.data_manager.get_user_data(user_id)
            text += get_add_text(true_add, add_length, niuniu_name, user_data)
            now_hardness = user_data['hardness']
            text += f"💪 {niuniu_name}的硬度增加{add_hardness}级，当前硬度：{now_hardness}\n"
        elif result == '无变化':
            text += f'🈚 {niuniu_name}的长度和硬度均没发生变化'
        elif result == '减少长度硬度不变':
            del_length = random_normal_distribution_int(1, 11, 2)
            self.data_manager.del_length(group_id, user_id, del_length)
            user_data = self.data_manager.get_user_data(user_id)
            text += f"📏 {niuniu_name}的长度减少了{del_length}cm，当前长度：{format_length(user_data['length'])}\n"
            text += f'💪 {niuniu_name}的硬度没有发生变化'
        elif result == '减少双属性':
            del_length = random_normal_distribution_int(1, 11, 2)
            del_hardness = random_normal_distribution_int(1, 4, 1)
            self.data_manager.del_hardness(group_id, user_id, del_hardness)
            self.data_manager.del_length(group_id, user_id, del_length)
            user_data = self.data_manager.get_user_data(user_id)
            text += f"📏 {niuniu_name}的长度减少了{del_length}cm，当前长度：{format_length(user_data['length'])}\n"
            text += f"💪 {niuniu_name}的硬度减少了{del_hardness}级，当前硬度：{format_length(user_data['hardness'])}\n"

        return text
