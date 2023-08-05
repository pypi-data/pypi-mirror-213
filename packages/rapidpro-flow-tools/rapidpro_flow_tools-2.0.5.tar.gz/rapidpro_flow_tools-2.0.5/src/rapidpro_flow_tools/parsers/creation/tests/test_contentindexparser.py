import unittest
import json

from rapidpro_flow_tools.parsers.creation.tests.mock_sheetreader import MockSheetReader
from rapidpro_flow_tools.parsers.creation.contentindexparser import ContentIndexParser
from rapidpro_flow_tools.parsers.creation.tests.utils import traverse_flow, Context

class TestParsing(unittest.TestCase):

    def compare_messages(self, render_output, flow_name, messages_exp, context=None):
        flow_found = False
        for flow in render_output["flows"]:
            if flow["name"] == flow_name:
                flow_found = True
                actions = traverse_flow(flow, context or Context())
                actions_exp = list(zip(['send_msg']*len(messages_exp), messages_exp))
                self.assertEqual(actions, actions_exp)
        if not flow_found:
            self.assertTrue(False, msg=f'Flow with name "{flow_name}" does not exist in output.')

    def test_basic_template_definition(self):
        ci_sheet = (
            'type,sheet_name,data_sheet,data_row_id,new_name,data_model,status\n'
            'template_definition,my_template,,,,,\n'
            'template_definition,my_template2,,,,,draft\n'
        )
        my_template = (
            'row_id,type,from,message_text\n'
            ',send_message,start,Some text\n'
        )

        sheet_reader = MockSheetReader(ci_sheet, {'my_template' : my_template})
        ci_parser = ContentIndexParser(sheet_reader)
        template_sheet = ci_parser.get_template_sheet('my_template')
        self.assertEqual(template_sheet.table[0][1], 'send_message')
        self.assertEqual(template_sheet.table[0][3], 'Some text')
        with self.assertRaises(KeyError):
            ci_parser.get_template_sheet('my_template2')

    def test_basic_nesting(self):
        ci_sheet = (
            'type,sheet_name,data_sheet,data_row_id,new_name,data_model,status\n'
            'template_definition,my_template,,,,,\n'
            'content_index,ci_sheet2,,,,,\n'
        )
        ci_sheet2 = (
            'type,sheet_name,data_sheet,data_row_id,new_name,data_model,status\n'
            'template_definition,my_template2,,,,,\n'
        )
        my_template = (
            'row_id,type,from,message_text\n'
            ',send_message,start,Some text\n'
        )
        my_template2 = (
            'row_id,type,from,message_text\n'
            ',send_message,start,Other text\n'
        )
        sheet_dict = {
            'ci_sheet2' : ci_sheet2,
            'my_template' : my_template,
            'my_template2' : my_template2,
        }

        sheet_reader = MockSheetReader(ci_sheet, sheet_dict)
        ci_parser = ContentIndexParser(sheet_reader)
        template_sheet = ci_parser.get_template_sheet('my_template')
        self.assertEqual(template_sheet.table[0][3], 'Some text')
        template_sheet = ci_parser.get_template_sheet('my_template2')
        self.assertEqual(template_sheet.table[0][3], 'Other text')

    def test_basic_user_model(self):
        ci_sheet = (
            'type,sheet_name,data_sheet,data_row_id,new_name,data_model,status\n'
            'data_sheet,simpledata,,,,SimpleRowModel,\n'
        )
        simpledata = (
            'ID,value1,value2\n'
            'rowA,1A,2A\n'
            'rowB,1B,2B\n'
        )

        sheet_reader = MockSheetReader(ci_sheet, {'simpledata' : simpledata})
        ci_parser = ContentIndexParser(sheet_reader, 'parsers.creation.tests.datarowmodels.simplemodel')
        datamodelA = ci_parser.get_data_model_instance('simpledata', 'rowA')
        datamodelB = ci_parser.get_data_model_instance('simpledata', 'rowB')
        self.assertEqual(datamodelA.value1, '1A')
        self.assertEqual(datamodelA.value2, '2A')
        self.assertEqual(datamodelB.value1, '1B')
        self.assertEqual(datamodelB.value2, '2B')

    def test_concat(self):
        ci_sheet = (
            'type,sheet_name,data_sheet,data_row_id,new_name,data_model,status\n'
            'data_sheet,simpleA;simpleB,,,simpledata,SimpleRowModel,\n'
        )
        simpleA = (
            'ID,value1,value2\n'
            'rowA,1A,2A\n'
        )
        simpleB = (
            'ID,value1,value2\n'
            'rowB,1B,2B\n'
        )
        sheet_dict = {
            'simpleA' : simpleA,
            'simpleB' : simpleB,
        }

        sheet_reader = MockSheetReader(ci_sheet, sheet_dict)
        ci_parser = ContentIndexParser(sheet_reader, 'parsers.creation.tests.datarowmodels.simplemodel')
        datamodelA = ci_parser.get_data_model_instance('simpledata', 'rowA')
        datamodelB = ci_parser.get_data_model_instance('simpledata', 'rowB')
        self.assertEqual(datamodelA.value1, '1A')
        self.assertEqual(datamodelA.value2, '2A')
        self.assertEqual(datamodelB.value1, '1B')
        self.assertEqual(datamodelB.value2, '2B')

    def test_generate_flows(self):
        ci_sheet = (
            'type,sheet_name,data_sheet,data_row_id,new_name,data_model,status\n'
            'create_flow,my_template,nesteddata,row1,,,\n'
            'create_flow,my_template,nesteddata,row2,,,\n'
            'create_flow,my_basic_flow,,,,,\n'
            'data_sheet,nesteddata,,,,NestedRowModel,\n'
        )
        # The templates are instantiated implicitly with all data rows
        ci_sheet_alt = (
            'type,sheet_name,data_sheet,data_row_id,new_name,data_model,status\n'
            'create_flow,my_template,nesteddata,,,,\n'
            'create_flow,my_basic_flow,,,,,\n'
            'data_sheet,nesteddata,,,,NestedRowModel,\n'
        )
        nesteddata = (
            'ID,value1,custom_field.happy,custom_field.sad\n'
            'row1,Value1,Happy1,Sad1\n'
            'row2,Value2,Happy2,Sad2\n'
            'row3,Value3,Happy3,Sad3\n'
        )
        my_template = (
            'row_id,type,from,message_text\n'
            ',send_message,start,{{value1}}\n'
            ',send_message,,{{custom_field.happy}} and {{custom_field.sad}}\n'
        )
        my_basic_flow = (
            'row_id,type,from,message_text\n'
            ',send_message,start,Some text\n'
        )
        sheet_dict = {
            'nesteddata' : nesteddata,
            'my_template' : my_template,
            'my_basic_flow' : my_basic_flow,
        }

        sheet_reader = MockSheetReader(ci_sheet, sheet_dict)
        ci_parser = ContentIndexParser(sheet_reader, 'parsers.creation.tests.datarowmodels.nestedmodel')
        container = ci_parser.parse_all_flows()
        render_output = container.render()
        self.compare_messages(render_output, 'my_basic_flow', ['Some text'])
        self.compare_messages(render_output, 'my_template - row1', ['Value1', 'Happy1 and Sad1'])
        self.compare_messages(render_output, 'my_template - row2', ['Value2', 'Happy2 and Sad2'])

        sheet_reader = MockSheetReader(ci_sheet_alt, sheet_dict)
        ci_parser = ContentIndexParser(sheet_reader, 'parsers.creation.tests.datarowmodels.nestedmodel')
        container = ci_parser.parse_all_flows()
        render_output = container.render()
        self.compare_messages(render_output, 'my_basic_flow', ['Some text'])
        self.compare_messages(render_output, 'my_template - row1', ['Value1', 'Happy1 and Sad1'])
        self.compare_messages(render_output, 'my_template - row2', ['Value2', 'Happy2 and Sad2'])
        self.compare_messages(render_output, 'my_template - row3', ['Value3', 'Happy3 and Sad3'])

    def test_bulk_flows_with_args(self):
        ci_sheet = (
            'type,sheet_name,data_sheet,data_row_id,template_arguments,new_name,data_model,status\n'
            'template_definition,my_template,,,arg1;arg2,,,\n'
            'create_flow,my_template,nesteddata,,ARG1;ARG2,my_renamed_template,,\n'
            'data_sheet,nesteddata,,,,,NestedRowModel,\n'
        )
        nesteddata = (
            'ID,value1,custom_field.happy,custom_field.sad\n'
            'row1,Value1,Happy1,Sad1\n'
            'row2,Value2,Happy2,Sad2\n'
        )
        my_template = (
            'row_id,type,from,message_text\n'
            ',send_message,start,{{value1}} {{arg1}} {{arg2}}\n'
            ',send_message,,{{custom_field.happy}} and {{custom_field.sad}}\n'
        )
        sheet_dict = {
            'nesteddata' : nesteddata,
            'my_template' : my_template,
        }

        sheet_reader = MockSheetReader(ci_sheet, sheet_dict)
        ci_parser = ContentIndexParser(sheet_reader, 'parsers.creation.tests.datarowmodels.nestedmodel')
        container = ci_parser.parse_all_flows()
        render_output = container.render()
        self.compare_messages(render_output, 'my_renamed_template - row1', ['Value1 ARG1 ARG2', 'Happy1 and Sad1'])
        self.compare_messages(render_output, 'my_renamed_template - row2', ['Value2 ARG1 ARG2', 'Happy2 and Sad2'])

    def test_insert_as_block(self):
        ci_sheet = (
            'type,sheet_name,data_sheet,data_row_id,new_name,data_model,status\n'
            'template_definition,my_template,,,,,\n'
            'create_flow,my_basic_flow,,,my_renamed_basic_flow,,\n'
            'data_sheet,nesteddata,,,,NestedRowModel,\n'
        )
        nesteddata = (
            'ID,value1,custom_field.happy,custom_field.sad\n'
            'row1,Value1,Happy1,Sad1\n'
            'row2,Value2,Happy2,Sad2\n'
        )
        my_template = (
            'row_id,type,from,condition,message_text\n'
            ',send_message,start,,{{value1}}\n'
            '1,wait_for_response,,,\n'
            ',send_message,1,happy,I\'m {{custom_field.happy}}\n'
            ',send_message,1,sad,I\'m {{custom_field.sad}}\n'
            ',hard_exit,,,\n'
            ',send_message,1,,I\'m something\n'
        )
        my_basic_flow = (
            'row_id,type,from,message_text,data_sheet,data_row_id\n'
            ',send_message,start,Some text,,\n'
            '1,insert_as_block,,my_template,nesteddata,row1\n'
            ',send_message,,Next message 1,,\n'
            ',insert_as_block,,my_template,nesteddata,row2\n'
            ',send_message,,Next message 2,,\n'
            ',go_to,,1,,\n'
        )
        sheet_dict = {
            'nesteddata' : nesteddata,
            'my_template' : my_template,
            'my_basic_flow' : my_basic_flow,
        }

        sheet_reader = MockSheetReader(ci_sheet, sheet_dict)
        ci_parser = ContentIndexParser(sheet_reader, 'parsers.creation.tests.datarowmodels.nestedmodel')
        container = ci_parser.parse_all_flows()
        render_output = container.render()
        messages_exp = [
            'Some text',
            'Value1',
            "I'm Happy1",
            'Next message 1',
            'Value2',
            "I'm something",
            'Next message 2',
            'Value1',
            "I'm Sad1",  # we're taking the hard exit now, leaving the flow.
        ]
        self.compare_messages(render_output, 'my_renamed_basic_flow', messages_exp, Context(inputs=['happy', 'else', 'sad']))

    def test_insert_as_block_with_sheet_arguments(self):
        ci_sheet = (
            'type,sheet_name,data_sheet,data_row_id,template_arguments,new_name,data_model,status\n'
            'template_definition,my_template,,,lookup;sheet|,,,\n'
            'create_flow,my_template,nesteddata,row3,string_lookup,,,\n'
            'create_flow,my_basic_flow,,,,,,\n'
            'data_sheet,nesteddata,,,,,ListRowModel,\n'
            'data_sheet,string_lookup,,,,,LookupRowModel,\n'
        )
        nesteddata = (
            'ID,messages.1,messages.2\n'
            'row1,hello,nicetosee\n'
            'row2,nicetosee,bye\n'
            'row3,hello,bye\n'
        )
        string_lookup = (
            'ID,happy,sad,neutral\n'
            'hello,Hello :),Hello :(,Hello\n'
            'bye,Bye :),Bye :(,Bye\n'
            'nicetosee,Nice to see you :),Not nice to see you :(,Nice to see you\n'
        )
        my_template = (
            'row_id,type,from,condition,message_text\n'
            '1,split_by_value,,,@field.mood\n'
            ',send_message,1,happy,{% for msg in messages %}{{lookup[msg].happy}}{% endfor %}\n'
            ',send_message,1,sad,{% for msg in messages %}{{lookup[msg].sad}}{% endfor %}\n'
            ',send_message,1,,{% for msg in messages %}{{lookup[msg].neutral}}{% endfor %}\n'
        )
        my_basic_flow = (
            'row_id,type,from,message_text,data_sheet,data_row_id,template_arguments\n'
            ',send_message,start,Some text,,,\n'
            ',insert_as_block,,my_template,nesteddata,row1,string_lookup\n'
            ',send_message,,Intermission,,,\n'
            ',insert_as_block,,my_template,nesteddata,row2,string_lookup\n'
        )
        sheet_dict = {
            'nesteddata' : nesteddata,
            'my_template' : my_template,
            'my_basic_flow' : my_basic_flow,
            'string_lookup' : string_lookup,
        }

        sheet_reader = MockSheetReader(ci_sheet, sheet_dict)
        ci_parser = ContentIndexParser(sheet_reader, 'parsers.creation.tests.datarowmodels.listmodel')
        container = ci_parser.parse_all_flows()
        render_output = container.render()
        messages_exp = [
            'Some text',
            'Hello :)Nice to see you :)',
            'Intermission',
            'Nice to see you :)Bye :)',
        ]
        self.compare_messages(render_output, 'my_basic_flow', messages_exp, Context(variables={'@field.mood':'happy'}))
        messages_exp = [
            'Some text',
            'Hello :(Not nice to see you :(',
            'Intermission',
            'Not nice to see you :(Bye :(',
        ]
        self.compare_messages(render_output, 'my_basic_flow', messages_exp, Context(variables={'@field.mood':'sad'}))
        messages_exp = [
            'Some text',
            'HelloNice to see you',
            'Intermission',
            'Nice to see youBye',
        ]
        self.compare_messages(render_output, 'my_basic_flow', messages_exp, Context(variables={'@field.mood':'something else'}))

        messages_exp = [
            'Hello :)Bye :)',
        ]
        self.compare_messages(render_output, 'my_template - row3', messages_exp, Context(variables={'@field.mood':'happy'}))


    def test_insert_as_block_with_arguments(self):
        ci_sheet = (
            'type,sheet_name,data_sheet,data_row_id,template_arguments,new_name,data_model,status\n'
            'template_definition,my_template,,,arg1|arg2;;default2,,,\n'
            'create_flow,my_template,,,value1,my_template_default,,\n'
            'create_flow,my_template,,,value1;value2,my_template_explicit,,\n'
        )
        my_template = (
            'row_id,type,from,condition,message_text\n'
            ',send_message,,,{{arg1}} {{arg2}}\n'
        )
        sheet_dict = {
            'my_template' : my_template,
        }

        sheet_reader = MockSheetReader(ci_sheet, sheet_dict)
        ci_parser = ContentIndexParser(sheet_reader, 'parsers.creation.tests.datarowmodels.listmodel')
        container = ci_parser.parse_all_flows()
        render_output = container.render()
        messages_exp = [
            'value1 default2',
        ]
        self.compare_messages(render_output, 'my_template_default', messages_exp)
        messages_exp = [
            'value1 value2',
        ]
        self.compare_messages(render_output, 'my_template_explicit', messages_exp)


    def test_eval(self):
        ci_sheet = (
            'type,sheet_name,data_sheet,data_row_id,new_name,data_model,template_arguments,status\n'
            'template_definition,flow,,,,,metadata;sheet|,\n'
            'data_sheet,content,,,,EvalContentModel,,\n'
            'data_sheet,metadata,,,,EvalMetadataModel,,\n'
            'create_flow,flow,content,,,,metadata,\n'
        )
        metadata = (
            'ID,include_if\n'
            'a,text\n'
        )
        flow = (
            '"row_id","type","from","loop_variable","include_if","message_text"\n'
            ',"send_message",,,,"hello"\n'
            ',"send_message",,,"{@metadata[""a""].include_if|eval == ""yes""@}","{{text}}"\n'
        )
        content = (
            'ID,text\n'
            'id1,yes\n'
            'id2,no\n'
        )
        sheet_dict = {
            'metadata' : metadata,
            'content' : content,
            'flow' : flow,
        }

        sheet_reader = MockSheetReader(ci_sheet, sheet_dict)
        ci_parser = ContentIndexParser(sheet_reader, 'parsers.creation.tests.datarowmodels.evalmodels')
        container = ci_parser.parse_all_flows()
        render_output = container.render()
        messages_exp = [
            'hello', 'yes',
        ]
        self.compare_messages(render_output, 'flow - id1', messages_exp)
        messages_exp = [
            'hello',
        ]
        self.compare_messages(render_output, 'flow - id2', messages_exp)
