#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
This programs aims at generating documentation for analyzers and responders by reading .json file of each neuron and generate associated .md file based upon output_page.md samples.


- docs/index.md
- docs/analyzers/NAME/flavor.md
- docs/responders/NAME/flavor.md
- docs/assets
- images/


This program also build the mkdocs file that will be used to generate and publish.
"""

from os import listdir, chdir, path, makedirs
from shutil import copy
from mdutils.mdutils import MdUtils
from mdutils import Html
import yaml
import json
import re


def neuron2md(nt,neuron, doc_path):
  """
  name: str (analyzers or responders)
  neuron: str
  doc_path: str
  """

  # Title 
  neuron_path =path.join(nt,neuron)
  mdFile = MdUtils(file_name="{}.md".format(neuron),title="")
  mdFile.new_header(level=1, title=neuron)

  
  #print(neuron)
    # Analyzers or Responders flavors
  for f in listdir(path.join(nt,neuron)):
    if nt in ["analyzers", "responders"] and f.endswith(".json"):
      with open(path.join(neuron_path, f),'r') as fc:
        config = json.load(fc)
        # Logo
        if config.get('service_logo'):
          logo_path = config.get('service_logo').get('path')
          logo_src_path = path.join(neuron_path,config.get('service_logo').get('path'))
          if path.exists(logo_src_path):
            ext = logo_path.split('.')[-1]
            logo_md_name = "{}_logo.{}".format(f.split('.')[0],ext)
            logo_md_path = path.join("assets", logo_md_name)
            logo_dest_path = path.join(doc_path,nt,logo_md_path)
            copy(logo_src_path, logo_dest_path)
            mdFile.new_line(mdFile.new_inline_image(text="service_logo", path=logo_md_path))

        mdFile.new_line()

        # Description and README.md file 
        if 'README.md' in listdir(neuron_path):
          readme = open("{}/README.md".format(neuron_path), 'r')
          mdFile.new_line("!!! tip \"Developer notes\"")
          mdFile.new_paragraph("    {}".format(readme.read().replace('\n','\n    ')))
          readme.close

        mdFile.new_header(level=2, title=config.get('name'))
        mdFile.new_line("!!! note \"\"")
        mdFile.new_line("    **Author**: _{}_".format(config.get('author')))
        mdFile.new_line("    **License**: _{}_".format(config.get('license')))
        mdFile.new_line("    **Version**: _{}_".format(config.get('version')))
        mdFile.new_line("    **Supported observables types**: _{}_".format(config.get('dataTypeList')))
        mdFile.new_line("    **Registration required**: \
          _{}_".format(config.get('registration_required','N/A')))
        mdFile.new_line("    **Subscription required**: \
          _{}_".format(config.get('subscription_required','N/A')))
        mdFile.new_line("    **Free subscription**: \
          _{}_".format(config.get('free_subscription','N/A')))
        mdFile.new_line('    **Third party service**: '+\
          mdFile.new_inline_link(link=config.get('service_homepage', 'N/A'), text=config.get('service_homepage', 'N/A')))
        
        mdFile.new_line()
        mdFile.new_header(level=3, title='Description')
        mdFile.new_paragraph(config.get('description', 'N/A'))
    
      
        mdFile.new_line()
        mdFile.new_header(level=3, title='Configuration')
        
        if config.get('configurationItems') and len(config.get('configurationItems')) > 0:
          for c in config.get('configurationItems'):
            configuration_items = ["**{}**".format(c.get('name')), c.get('description', 'No description')]
            configuration_items.extend(["**Default value if not configured**",  "_{}_".format(c.get('default', 'N/A'))])
            configuration_items.extend(["**Type of the configuration item**",  "_{}_".format(c.get('type'))])
            configuration_items.extend(["**The configuration item can contain multiple values**",  "_{}_".format(c.get('multi'))])
            configuration_items.extend(["**Is required**",  "_{}_".format(c.get('required'))])
            mdFile.new_line()
            mdFile.new_table(columns=2, rows=5, text=configuration_items, text_align='left')

        else:
          mdFile.new_paragraph("No specific configuration required.")
    
    
    # Analysers report samples 
    if nt == "analyzers" and f.endswith(".json"):
      # Templates for TheHive
      mdFile.new_line()
      mdFile.new_header(level=3, title='Templates samples for TheHive')

      ## Copy images files to destination folder
      base_neuronname = f.split('.')[0]
      if config.get('screenshots'):
        for idx, sc in enumerate(config.get('screenshots')):
          sc_path = sc.get('path')
          sc_src_path = path.join(neuron_path,sc.get('path'))
          if path.exists(sc_src_path):
            sc_filename = path.basename(sc.get('path'))
            ext = sc_filename.split('.')[-1]
            sc_filename="{}_{}.{}".format(base_neuronname,idx,ext)
            sc_md_path = path.join("assets",sc_filename)
            sc_dest_path =path.join(doc_path,nt,sc_md_path)
            copy(sc_src_path, sc_dest_path)
            mdFile.new_paragraph(mdFile.new_inline_image(text=sc.get('caption','screenshot'), path=sc_md_path))
      else:
        mdFile.new_paragraph("No template samples to display.")

  # Save md file
  dest_dir = path.join(doc_path, nt)
  if not path.exists(dest_dir):
    makedirs(dest_dir)
  olddir = path.abspath(path.curdir)
  chdir(dest_dir)
  mdFile.create_md_file()
  chdir(olddir)
 

def build_mkdocs(md_path, mkdocs_filename):
  # md_path = 'docs/'
  nt = ['analyzers', 'responders']
  analyzers= []
  responders = []

  for a in nt:
    for n in sorted(listdir(path.join(md_path, a))):
      if n not in ['assets']:
        if a == "analyzers":
          analyzers.append({n.split('.')[0]:path.join(a,n)})
        else:
          responders.append({n.split('.')[0]:path.join(a,n)})

  mkdocs = """
    site_name: Cortex Neurons documentation      
    theme:
        name: 'material'
        logo: 'images/cortex-logo.png'
        palette:
          primary: 'blue'
          accent: blue

    extra:
      social:
        - icon: fontawesome/solid/home
          link: "https://www.thehive-project.org"
        - icon: fontawesome/brands/wordpress
          link: "https://blog.thehive-project.org"
        - icon: fontawesome/brands/twitter
          link: "https://twitter.com/TheHive_Project"
        - icon: fontawesome/brands/github
          link: "https://github.com/TheHive-Project"
        - icon: fontawesome/brands/gitter
          link: "https://gitter.im/TheHive-Project/TheHive"
    repo_name: "Cortex-Neurons"
    repo_url: "https://github.com/TheHive-Project/Cortex-Analyzers"
    markdown_extensions:
        - toc:
            permalink: "#"
        - codehilite
        - admonition
        - pymdownx.superfences
        - pymdownx.tabbed
    plugins:
        - search
        - awesome-pages:
            filename: .md
    extra_css:
        - css/pdf.css
  """
  mkdocs_nav_part1 = """
  nav:
          - Home: 'README.md'
  """
  mkdocs_nav_part2 = """
          - 'Changelog': 'CHANGELOG.md'
          - 'Code of Conduct': 'code_of_conduct.md'
          - 'Developers guides':
            - 'Analyzer definition': 'analyzers_definition.md'
            - 'How to write an Analyzer': 'how-to-create-an-analyzer.md'
  """
  mk = yaml.safe_load(mkdocs)
  nav1 = yaml.safe_load(mkdocs_nav_part1)
  nav2 = yaml.safe_load(mkdocs_nav_part2)
  nav1.get('nav').append({'Analyzers':analyzers})
  nav1.get('nav').append({'Responders':responders})
  nav1['nav'] = nav1.get('nav')+nav2
  mk.update(nav1)
  
  with open(mkdocs_filename, 'w') as yml:
    yml.write(yaml.dump(mk))
  yml.close()

def run():
  doc_path = "./docs" 
  mkdocs_filename = "./mkdocs.yml" 
  # Build md file for each neuron and build files tree
  for nt in ["analyzers", "responders"] :
    if path.exists(nt):
      for neuron in [d for d in listdir(nt) if path.isdir(path.join(nt,d))]:
        neuron2md(nt, neuron, doc_path)
  
  # Build mkdocs file
  build_mkdocs(doc_path, mkdocs_filename)

if __name__ == '__main__':
  run()
