from nose.plugins import Plugin
from nose.pyversion import format_exception
import logging
import time
import os 
import jinja2


class Junit2Html(Plugin):
    name = 'html'
    def __init__(self):
        super(Junit2Html, self).__init__()
        self._envrionment = jinja2.Environment()
        self._load_template()

    def options(self, parser, env=os.environ):
        Plugin.options(self, parser, env)
        parser.add_option(
            '--html-testsuite-name', action='store',
            dest='testsuite_name', metavar="PACKAGE",
            default=env.get('NOSE_TESTSUITE_NAME', 'Nosetests'),
            help=("Name of the testsuite."
                  "Default testsuite name is Nosetests."))
        
        parser.add_option(
            '--html-file', action='store',
            dest='html_file', metavar="FILE",
            default=env.get('NOSE_HTML_FILE', 'nosetests.html'),
            help=("html file to store the report in."
                  "Default is nosetests.html in."))

    def configure(self, options, config):
        Plugin.configure(self, options, config)
        config.options.noSkip = True
        if self.enabled:
            self.result = dict(summary={}, testcases=[])
            self.result['summary'] = {'errors': 0,
                                      'failures': 0,
                                      'passed': 0,
                                      'skip': 0
                                    }
            self.errorlist = []
            self.testsuite_name = options.testsuite_name
            self.output_file = options.html_file

    def beforeTest(self, test):
        self.start_time = time.time()

    def report(self, stream):
        """Writes an Xunit-formatted XML file

        The file includes a report of test errors and failures.

        """
        
        self.result['summary']['name'] = self.testsuite_name
        self.result['summary']['tests'] = self.result['summary']['errors'] + \
                                          self.result['summary']['failures'] + \
                                          self.result['summary']['passed'] + \
                                          self.result['summary']['skip']
        html = self._generate_html(self.result)
        self._export_html(html, self.output_file)
        stream.writeln('-' * 70)
        stream.writeln('html generated at {}/{}'.format(os.path.abspath('.'), self.output_file))

    def addError(self, test, err):
        """Add error output to Xunit report.
        """
        taken = self.timeTaken()
        time_taken = '{0:.5f}'.format(taken)
        result = dict()
        trace_back = format_exception(err, 'UTF-8')
        if (err[0].__name__ == 'SkipTest'):
            self.result['summary']['skip'] += 1
            result['status'] = 'skipped'
            trace_back = trace_back.strip('Exceptions: ')
        else:
            self.result['summary']['errors'] += 1
            result['status'] = 'errored'
        
        result['time'] = time_taken
        result['id'] = test.id()
        result['details'] = {'message': trace_back}
        self.result['testcases'].append(result)

    def addFailure(self, test, err, capt=None, tb_info=None):
        """Add failure output to Xunit report.
        """
        taken = self.timeTaken()
        time_taken = '{0:.5f}'.format(taken)
        result = dict()
        trace_back = format_exception(err, 'UTF-8')
        self.result['summary']['failures'] += 1
        result['time'] = time_taken
        result['id'] = test.id()
        result['details'] = {'message': trace_back}
        result['status'] = 'failed'
        self.result['testcases'].append(result)

    def addSuccess(self, test, capt=None):
        """Add success output to Xunit report.
        """
        taken = self.timeTaken()
        time_taken = '{0:.5f}'.format(taken)
        result = dict()
        self.result['summary']['passed'] += 1
        result['time'] = time_taken
        result['id'] = test.id()
        result['status'] = 'Passed'
        self.result['testcases'].append(result)
    
    def addSkip(self, test):
        import ipdb; ipdb.set_trace()
        self.result['summary']['skipped'] += 1

    def timeTaken(self):
        taken = time.time() - self.start_time
        return taken

    def _generate_html(self, result):
        template = self._envrionment.from_string(self._template)
        html = template.render(** result)
        return html
    
    def _export_html(self, html, path="."):
        with open(path, "w") as f:
            f.write(html)

    def _load_file(self, path):
        with open(path, "r") as f:
            content = f.read()
        return content

    def _load_template(self):
        path = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(path, "template.html")
        self._template = self._load_file(template_path)
