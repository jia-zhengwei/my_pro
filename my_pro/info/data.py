# coding: utf-8


class DataOperation(object):
    """
    对数据进行处理：对字典数据中的列表进行处理，返回一个处理完的数据体
    """

    def __init__(self, data):
        self.data = data

    def update_data(self):
        """
        从excel中获取的数据进行处理，对字典value值遍历处理，返回特定的数据格式
        :return: 返回列表数据
        """

        a = []
        num = 1
        new_list = []
        b = 1

        for j in self.data.keys():
            name = j

        for i in dict(self.data)[name]:
            if len(i) >= b:
                b = len(i)

        for i in dict(self.data)[name]:
            if not i[0] is None:
                num = 1
                a = i
                list_one = [None] * (b - len(i))
                for li in list_one:
                    i.append(li)
                i.append(num)
                num += 1
            if i[0] is None:
                i[0] = a[0]
                list_one = [None] * (b - len(i))
                for li in list_one:
                    i.append(li)
                i.append(num)
                num += 1

            new_list.append(i)
        return new_list

    @staticmethod
    def data_process(list_data):
        """
        处理过程流程分析的数据
        :param: list_data: 由update_data()返回的列表数据（list_data）
        :return: 返回字典数据
        """
        data_dict = {}
        for i in list_data[2:]:
            if i[0] in data_dict.keys():
                try:
                    data_dict[i[0]]['input_variation'][str(i[-1])] = i[6]
                    data_dict[i[0]]['product_features'][str(i[-1])] = i[7]
                    data_dict[i[0]]['procedure_variation'][str(i[-1])] = i[8]
                except IndexError:
                    continue
            else:
                data_dict[i[0]] = {}
                data_dict[i[0]]['procedure_name'] = i[1]
                data_dict[i[0]]['procedure_spec'] = {}
                data_dict[i[0]]['input_variation'] = {}
                data_dict[i[0]]['product_features'] = {}
                data_dict[i[0]]['procedure_variation'] = {}
                data_dict[i[0]]['procedure_spec']['manualfacture'] = i[2]
                data_dict[i[0]]['procedure_spec']['move'] = i[3]
                data_dict[i[0]]['procedure_spec']['storage'] = i[4]
                data_dict[i[0]]['procedure_spec']['inspect'] = i[5]
                data_dict[i[0]]['input_variation'][str(i[-1])] = i[6]
                data_dict[i[0]]['product_features'][str(i[-1])] = i[7]
                data_dict[i[0]]['procedure_variation'][str(i[-1])] = i[8]

        return data_dict

    @staticmethod
    def data_failure(list_data):
        """
        处理失效模式分析的数据
        :param list_data: 由updata_data()返回的列表数据（list_data）
        :return: 返回处理好的字典数据
        """
        data_dict = {}
        # 忽略表头
        for i in list_data[2:]:
            if i[0] in data_dict.keys():
                try:
                    data_dict[i[0]]['requirement'][str(i[-1])] = i[1]
                    data_dict[i[0]]['potential_failure_mode'][str(i[-1])] = i[2]
                    data_dict[i[0]]['potential_failure_effects'][str(i[-1])] = i[3]
                    data_dict[i[0]]['severity'][str(i[-1])] = i[4]
                    data_dict[i[0]]['classification'][str(i[-1])] = i[5]
                    data_dict[i[0]]['potential_failure_causes'][str(i[-1])] = i[6]
                    data_dict[i[0]]['controls_prevention'][str(i[-1])] = i[7]
                    data_dict[i[0]]['occurrence'][str(i[-1])] = i[8]
                    data_dict[i[0]]['controls_detection'][str(i[-1])] = i[9]
                    data_dict[i[0]]['detection'][str(i[-1])] = i[10]
                    data_dict[i[0]]['RPN'][str(i[-1])] = i[11]
                    data_dict[i[0]]['recommended_action'][str(i[-1])] = i[12]
                    data_dict[i[0]]['responsibility_completion_date'][str(i[-1])] = i[13]
                    data_dict[i[0]]['action_result']['actiontaken_complete_date'][str(i[-1])] = i[14]
                    data_dict[i[0]]['action_result']['severity'][str(i[-1])] = i[15]
                    data_dict[i[0]]['action_result']['occurrence'][str(i[-1])] = i[16]
                    data_dict[i[0]]['action_result']['detection'][str(i[-1])] = i[17]
                    data_dict[i[0]]['action_result']['RPN'][str(i[-1])] = i[18]
                except IndexError:
                    continue
            else:
                data_dict[i[0]] = {}
                data_dict[i[0]]['requirement'] = {}
                data_dict[i[0]]['potential_failure_mode'] = {}
                data_dict[i[0]]['potential_failure_effects'] = {}
                data_dict[i[0]]['severity'] = {}
                data_dict[i[0]]['classification'] = {}
                data_dict[i[0]]['potential_failure_causes'] = {}
                data_dict[i[0]]['controls_prevention'] = {}
                data_dict[i[0]]['occurrence'] = {}
                data_dict[i[0]]['controls_detection'] = {}
                data_dict[i[0]]['detection'] = {}
                data_dict[i[0]]['RPN'] = {}
                data_dict[i[0]]['recommended_action'] = {}
                data_dict[i[0]]['responsibility_completion_date'] = {}
                data_dict[i[0]]['action_result'] = {}
                data_dict[i[0]]['action_result']['actiontaken_complete_date'] = {}
                data_dict[i[0]]['action_result']['severity'] = {}
                data_dict[i[0]]['action_result']['occurrence'] = {}
                data_dict[i[0]]['action_result']['detection'] = {}
                data_dict[i[0]]['action_result']['RPN'] = {}

                data_dict[i[0]]['requirement'][str(i[-1])] = i[1]
                data_dict[i[0]]['potential_failure_mode'][str(i[-1])] = i[2]
                data_dict[i[0]]['potential_failure_effects'][str(i[-1])] = i[3]
                data_dict[i[0]]['severity'][str(i[-1])] = i[4]
                data_dict[i[0]]['classification'][str(i[-1])] = i[5]
                data_dict[i[0]]['potential_failure_causes'][str(i[-1])] = i[6]
                data_dict[i[0]]['controls_prevention'][str(i[-1])] = i[7]
                data_dict[i[0]]['occurrence'][str(i[-1])] = i[8]
                data_dict[i[0]]['controls_detection'][str(i[-1])] = i[9]
                data_dict[i[0]]['detection'][str(i[-1])] = i[10]
                data_dict[i[0]]['RPN'][str(i[-1])] = i[11]
                data_dict[i[0]]['recommended_action'][str(i[-1])] = i[12]
                data_dict[i[0]]['responsibility_completion_date'][str(i[-1])] = i[13]
                data_dict[i[0]]['action_result']['actiontaken_complete_date'][str(i[-1])] = i[14]
                data_dict[i[0]]['action_result']['severity'][str(i[-1])] = i[15]
                data_dict[i[0]]['action_result']['occurrence'][str(i[-1])] = i[16]
                data_dict[i[0]]['action_result']['detection'][str(i[-1])] = i[17]
                data_dict[i[0]]['action_result']['RPN'][str(i[-1])] = i[18]
        return data_dict

    @staticmethod
    def data_control(list_data):
        """
        处理控制计划分析的数据
        :param list_data: 由updata_data()返回的列表数据（list_data）
        :return: 返回处理好的字典数据
        """
        data_dict = {}

        for i in list_data[2:]:
            if i[0] in data_dict.keys():
                data_dict[i[0]]['machine'][str(i[-1])] = i[2]
                data_dict[i[0]]['characteristics']['NO'][str(i[-1])] = i[3]
                data_dict[i[0]]['characteristics']['product'][str(i[-1])] = i[4]
                data_dict[i[0]]['characteristics']['process'][str(i[-1])] = i[5]
                data_dict[i[0]]['special_char_class'][str(i[-1])] = i[6]
                data_dict[i[0]]['methods']['tolerance'][str(i[-1])] = i[7]
                data_dict[i[0]]['methods']['evaluation_technique'][str(i[-1])] = i[8]
                if isinstance(i[9], int):
                    data_dict[i[0]]['methods']['size'][str(i[-1])] = str((i[9]) * 100) + '%'
                else:
                    data_dict[i[0]]['methods']['size'][str(i[-1])] = i[9]
                data_dict[i[0]]['methods']['freq'][str(i[-1])] = i[10]
                data_dict[i[0]]['methods']['control_methods'][str(i[-1])] = i[11]
                data_dict[i[0]]['reaction_plan'][str(i[-1])] = i[12]
            else:
                data_dict[i[0]] = {}
                data_dict[i[0]]['process_name'] = i[1]
                data_dict[i[0]]['machine'] = {}
                data_dict[i[0]]['characteristics'] = {}
                data_dict[i[0]]['characteristics']['NO'] = {}
                data_dict[i[0]]['characteristics']['product'] = {}
                data_dict[i[0]]['characteristics']['process'] = {}
                data_dict[i[0]]['special_char_class'] = {}
                data_dict[i[0]]['methods'] = {}
                data_dict[i[0]]['methods']['tolerance'] = {}
                data_dict[i[0]]['methods']['evaluation_technique'] = {}
                data_dict[i[0]]['methods']['size'] = {}
                data_dict[i[0]]['methods']['freq'] = {}
                data_dict[i[0]]['methods']['control_methods'] = {}
                data_dict[i[0]]['reaction_plan'] = {}

                data_dict[i[0]]['machine'][str(i[-1])] = i[2]
                data_dict[i[0]]['characteristics']['NO'][str(i[-1])] = i[3]
                data_dict[i[0]]['characteristics']['product'][str(i[-1])] = i[4]
                data_dict[i[0]]['characteristics']['process'][str(i[-1])] = i[5]
                data_dict[i[0]]['special_char_class'][str(i[-1])] = i[6]
                data_dict[i[0]]['methods']['tolerance'][str(i[-1])] = i[7]
                data_dict[i[0]]['methods']['evaluation_technique'][str(i[-1])] = i[8]
                if isinstance(i[9], int):
                    data_dict[i[0]]['methods']['size'][str(i[-1])] = str((i[9]) * 100) + '%'
                else:
                    data_dict[i[0]]['methods']['size'][str(i[-1])] = i[9]
                data_dict[i[0]]['methods']['freq'][str(i[-1])] = i[10]
                data_dict[i[0]]['methods']['control_methods'][str(i[-1])] = i[11]
                data_dict[i[0]]['reaction_plan'][str(i[-1])] = i[12]
        return data_dict

    @staticmethod
    def data_special(list_data):
        """
        处理特殊清单的数据
        :param list_data: 由updata_data()返回的列表数据（list_data）
        :return: 返回处理好的字典数据
        """
        data_dict = {}

        for i in list_data[1:]:
            if i[0] in data_dict.keys():
                data_dict[i[0]]['process_special_characteristics'][str(i[-1])] = i[4]
                data_dict[i[0]]['special_characteristics_symbol'][str(i[-1])] = i[7]
                data_dict[i[0]]['regulatory_compliance'][str(i[-1])] = i[8]
                data_dict[i[0]]['safety'][str(i[-1])] = i[9]
                data_dict[i[0]]['function'][str(i[-1])] = i[10]
                data_dict[i[0]]['follow_process'][str(i[-1])] = i[11]
            else:
                data_dict[i[0]] = {}
                data_dict[i[0]]['process_name'] = i[1]
                data_dict[i[0]]['process_special_characteristics'] = {}
                data_dict[i[0]]['special_characteristics_symbol'] = {}
                data_dict[i[0]]['regulatory_compliance'] = {}
                data_dict[i[0]]['safety'] = {}
                data_dict[i[0]]['function'] = {}
                data_dict[i[0]]['follow_process'] = {}

                data_dict[i[0]]['process_special_characteristics'][str(i[-1])] = i[4]
                data_dict[i[0]]['special_characteristics_symbol'][str(i[-1])] = i[7]
                data_dict[i[0]]['regulatory_compliance'][str(i[-1])] = i[8]
                data_dict[i[0]]['safety'][str(i[-1])] = i[9]
                data_dict[i[0]]['function'][str(i[-1])] = i[10]
                data_dict[i[0]]['follow_process'][str(i[-1])] = i[11]
        return data_dict


if __name__ == '__main__':

    pass
