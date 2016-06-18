#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")
	
class PostHandler(BaseHandler):
	def post(self):
		#To Do
		string = "capitalized_text"
		some_text = self.request.get("some_text")
		return self.render_template("result.html", {
			"some_text": some_text,
			"capitalized_text": some_text.upper(),
			"string_length": len(some_text)
		})
	
class CalculatorHandler(BaseHandler):
	def get(self):
		return self.render_template("calculator.html")
	
	def post(self):
		number1 = self.request.get("number1")
		number2 = self.request.get("number2")
		return self.write(int(number1) + int(number2))
	
		#return self.render_template("calculator-result.html", {
			#"number1": number1,
			#"number2": number2
			
			#})
		
		
app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
	  webapp2.Route('/result', PostHandler),
	  webapp2.Route('/calculator', CalculatorHandler),
	  webapp2.Route('/calculator-result', CalculatorHandler),
], debug=True)
