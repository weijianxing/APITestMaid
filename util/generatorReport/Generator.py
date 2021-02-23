from datetime import datetime
import json
import sys

import os
import pdfkit
from jinja2 import Environment, FileSystemLoader


class Generator:

    # Constructor
    def __init__(self, appName = "" , templatePath= "" , reportPath= "",dataPath = ""):
        # Open json file
        if len(dataPath) == 0:
            realdataPath = 'util/Data/data.json'
        else:
            realdataPath = dataPath
        with open(realdataPath) as json_file:
            self.report_json = json.load(json_file)

        # Open json file
        #disable pdf generate.
        # with open('Data/pdf_options.json') as json_options_file:
        #     self.json_pdf_options = json.load(json_options_file)

        # Set the path of all json files
        if len(templatePath) == 0:
            self.path_to_template = 'util/Templates/'
        else:
            self.path_to_template = templatePath
        if len(reportPath) == 0:
            self.path_to_report = 'util/Report/'
        else:
            self.path_to_report = reportPath
        self.extension = '.pdf'
        self.htmlExtension = ".html"
        self.date = datetime.now().strftime("%a") + " " + datetime.now().strftime("%b") + " " + datetime.now().\
            strftime("%d") + " " + datetime.now().strftime("%Y")
        if len(appName) == 0:
            self.app = 'Python Testing Report Generator  '
        else:
            self.app = appName

    # Get the html template
    def get_template(self):
        print("current dir is : " + os.getcwd())
        env = Environment(loader=FileSystemLoader(self.path_to_template))

        template = env.get_template("template_wuage.html")
        return template

    # Render the template with the data
    def template_rendering(self):
        render_template = self.get_template()
        results = self.report_json
        date = self.date
        summary = self.get_total_element()
        total = summary['Passed'] + summary['Failed'] + summary['Skipped']
        template = render_template.render(title=self.app, results=results, date=date, summary=summary, total=total)
        return template
    def generate_html(self):
        date = self.date.replace(" ", "_")
        app = self.app.lower().replace(" ", "_").capitalize()
        file_name = str(self.path_to_report + app + date + self.htmlExtension)
        html = self.template_rendering()
        with open(file_name, 'w') as fh:
            fh.write(html)

        fh.close()
    # Generate the pdf file
    def generate_pdf(self):
        date = self.date.replace(" ", "_")
        app = self.app.lower().replace(" ", "_").capitalize()
        file_name = str(self.path_to_report + app + date + self.extension)
        html = self.template_rendering()
        if sys.platform == 'win32':
            path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
            pdfkit.from_string(html, file_name, options=self.json_pdf_options, configuration=config)
        elif sys.platform == 'linux':
            pdfkit.from_string(html, file_name, options=self.json_pdf_options)

    def get_total_element(self):
        length = len(self.report_json)
        total = dict()
        passed = 0
        failed = 0
        skipped = 0
        item = 0
        while length > 0:
            if self.report_json[item]['Result'] == 'Passed':
                passed += 1
                item += 1
                length -= 1
            elif self.report_json[item]['Result'] == 'Failed':
                failed += 1
                item += 1
                length -= 1
            else:
                skipped += 1
                item += 1
                length -= 1
        total['Passed'] = passed
        total['Skipped'] = skipped
        total['Failed'] = failed

        return total


# a = Generator()
# a.generate_html()

if __name__ == '__main__':

    a = Generator(appName="search_report", dataPath="util/Data/reportData.json")
    a.generate_html()