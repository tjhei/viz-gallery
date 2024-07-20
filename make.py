from jinja2 import Template
import os

template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
        }
        .header {
            display: flex;
            flex-direction: column;
            background-color: #f0f0f0;
            border-bottom: 1px solid #ccc;
        }
        .title-bar {
            display: flex;
            align-items: center;
            padding: 10px;
        }
        .home-button {
            padding: 10px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            margin-left: 10px;
            border-radius: 5px;
            cursor: pointer;
        }
        .tabs {
            display: flex;
            cursor: pointer;
            margin-left: 10px;
        }
        .tab {
            padding: 10px 20px;
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            border-bottom: none;
            margin-right: 5px;
        }
        .tab.active {
            background-color: #007bff;
            color: #fff;
        }
        .content {
            flex: 1;
            overflow: hidden;
        }
        iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="title-bar">
            <a class="home-button" href="index.html">Home</a>&nbsp;
            <h1>{{ title }}</h1>
        </div>
        <div class="tabs">
            {% for tab in tabs %}
            <div class="tab" data-tab="{{ tab.name }}" data-url="{{ tab.url }}">{{ tab.name }}</div>
            {% endfor %}
        </div>
    </div>
    <div class="content">
        <iframe id="content-frame" src="{{ tabs[0].url }}"></iframe>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const tabs = document.querySelectorAll('.tab');
            const iframe = document.getElementById('content-frame');

            function updateActiveTab(tab) {
                if (tab.classList.contains('active')) return; // Ignore clicks on the active tab
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                iframe.src = tab.dataset.url;
                history.pushState(null, '', `#${tab.dataset.tab}`);
            }

            tabs.forEach(tab => {
                tab.addEventListener('click', () => updateActiveTab(tab));
            });

            // Check the URL hash and set the active tab on page load
            const hash = window.location.hash;
            if (hash) {
                const tab = Array.from(tabs).find(t => t.dataset.tab === hash.substring(1));
                if (tab) {
                    updateActiveTab(tab);
                }
            }
        });
    </script>
</body>
</html>
"""

index_template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Index of Generated Pages</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        h1 {
            text-align: center;
        }
        .page-list {
            list-style-type: none;
            padding: 0;
        }
        .page-item {
            display: flex;
            align-items: center;
            margin: 10px 0;
        }
        .page-item img {
            width: 50px;
            height: 50px;
            margin-right: 20px;
        }
        .page-item a {
            text-decoration: none;
            color: #007bff;
        }
    </style>
</head>
<body>
    <h1>Index of Generated Pages</h1>
    <ul class="page-list">
        {% for page in pages %}
        <li class="page-item">
            <img src="{{ page.image }}" alt="Image for {{ page.title }}">
            <a href="{{ page.filename }}">{{ page.title }}</a>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
"""

def generate_page(title, tabs, output_filename):
    template = Template(template_str)
    html_content = template.render(title=title, tabs=tabs)
    
    with open(output_filename, 'w') as f:
        f.write(html_content)

def generate_index(pages):
    template = Template(index_template_str)
    html_content = template.render(pages=pages)
    
    with open('index.html', 'w') as f:
        f.write(html_content)

# Example usage
pages = [
    {
        'title': 'Test page 1',
        'tabs': [
            {'name': 'Tab 1', 'url': 'https://example.com/page1'},
            {'name': 'Tab 2', 'url': 'https://example.com/page2'},
            {'name': 'Tab 3', 'url': 'https://example.com/page3'}
        ],
        'output_filename': 'test1.html'
    },
    {
        'title': 'Cascadia subduction model',
        'tabs': [
            {'name': 'Glance', 'url': 'https://f.tjhei.info/glance/?name=cascadia_subduction-v1.glance&url=https://f.tjhei.info/view-cascadia-model-menno/cascadia_subduction_v1.glance'},
            {'name': 'Information', 'url': 'cascadia-info.html'}
        ],
        'output_filename': 'cascadia.html'
    },
    {
        'title': 'ASPECT 3d convection cookbook',
        'tabs': [
            {'name': 'vtkjs', 'url': 'https://f.tjhei.info/ase/?fileURL=https://f.tjhei.info/viz-gallery/convection3d/solution0021.vtkjs'},
            {'name': 'Glance', 'url': 'https://f.tjhei.info/glance/?name=view-convection_box.glance&url=https://f.tjhei.info/view-convection-box/convection_box.glance'},
            {'name': 'Information', 'url': 'convection3d-info.html'}
        ],
        'output_filename': 'convection3d.html'
    }
]

# Generate individual pages
for page in pages:
    generate_page(page['title'], page['tabs'], page['output_filename'])

# Prepare data for index.html generation
index_pages = [
    {
        'title': page['title'],
        'filename': page['output_filename'],
        'image': f"{os.path.splitext(page['output_filename'])[0]}.jpg"  # Assumes images are named like the HTML files
    }
    for page in pages
]

# Generate index.html
generate_index(index_pages)

print("Pages and index generated successfully!")
