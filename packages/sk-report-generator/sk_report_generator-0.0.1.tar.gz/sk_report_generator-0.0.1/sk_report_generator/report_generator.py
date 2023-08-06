import regex
import traceback
class ReportGenerator:



    def generate_report(self,template,data):

        for variable,value in data.items():
            pattern = r'(\s|\b|{)'+regex.escape(variable)+r'(\s|\b|})'
            find  = regex.search(pattern,template)
            if find:
                template = template.replace(find[0],find[0].replace(variable,str(value)))

        placeholder_pattern = r'{{[^{}]+}}'
        matches =  regex.findall(placeholder_pattern,template)

        for match in matches:
            main_part =match.replace('{','').replace('}','')
            result = main_part.split(':')
            flag = False
            try:
                value = float(result[0])
                format_rule = result[1].replace(' ','')
                if round(value%1,9)==0:
                    value = int(value) ##convert float into int if the float part is too small
                replacement =format(value, format_rule)

            except ValueError as error:
                error_message = str(error)
                if 'could not convert string to float' in error_message:
                    flag = True
                else:
                    replacement = f'({main_part}, {error_message})'

            except:
                flag = True

            if flag:

                if '$' in main_part:
                    replacement =match
                else:
                    replacement =main_part


            template = template.replace(match,replacement)


        return template
