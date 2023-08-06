from pelican import signals
from pelican.contents import Page, Static
from pelican.generators import StaticGenerator
from mailscrambler import javascriptify, deobfuscator
import re
import os

# Matching an email as a single group
EMAIL_REGEX = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'

class DeobfGenerator(object):
   def __init__(self, context, settings, path, theme, output_path, *null):
    self.context = context
    self.settings = settings
    self.output_path = output_path
    
   def generate_output(self, writer):
      # Adds deobf.js to output root
      path = os.path.join(self.output_path, "deobf.js")
      with open(path, "w") as f:
        f.write(deobfuscator().replace('<script type="text/javascript">', "").replace("</script>", "").strip())

def email_cloak(content: Page):
  all_emails = re.findall(EMAIL_REGEX, content._content)
  all_emails = [email if not email.endswith(".") else email[:-1] for email in all_emails]
  all_javascriptified_emails = [javascriptify(email, do_scramble=True) for email in all_emails]

  # Replace all plaintext e-mails with obfuscated e-mails
  for email, javascriptified_email in zip(all_emails, all_javascriptified_emails):
      content._content = content._content.replace(email, javascriptified_email)
  
  # Add a script tag at the end of the page to deobfuscate the emails
  if len(all_emails) > 0:
      # Insert before </body>
      content._content += "<script type=\"text/javascript\" src=\"/deobf.js\"></script>"
  
  return content._content

def _generator_write(generator, content: Page):
   email_cloak(content)

def _generator_enrich_context(generator):
    generator.context["javascriptify"] = javascriptify

def get_generators(generators):
  return DeobfGenerator

def register():
  signals.get_generators.connect(get_generators)
  signals.page_generator_init.connect(_generator_enrich_context)
  signals.page_generator_write_page.connect(_generator_write)
  signals.article_generator_init.connect(_generator_enrich_context)
  signals.article_generator_write_article.connect(_generator_write)