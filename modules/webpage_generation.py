def book_page(title, wordcolor):
    """
    Generates a webpage for the book.
    Compatible with flask template system
    """
    return f"""
    <html>
        <head>
            <meta charset="utf-8">
            <link rel="stylesheet" type="text/css" href="{{{{ url_for('static', filename='css/style.css') }}}}">
            <link rel="shortcut icon" type="image/png" href="{{{{ url_for('static', filename='css/style.css') }}}}"/>
            <title>{title}</title>
        </head>

        <body class="body">
            <table class="tablecategory">
                <tr class="rowcategory">
                    <td class="categorytitle" colspan="2">
                        <h1 class="bookcenter">{title}</h1>
                    </td>
                </tr>
                <tr class="bookrow">
                    <td class="tablecell" align="center">
                        <div class="bookbox">
                            <h2>Word cloud</h2>
                            <img width="82%" height="82%" src="{{{{ url_for('static', filename='output/wordclouds/{title}.jpg') }}}}">
                        </div>
                    </td>
                    <td class="tablecell">
                        <div class="bookbox" style="word-wrap: break-word;">
                            <h2>Color words</h2>
                            {wordcolor}
                        </div>
                    </td>
                </tr>
                <tr class="bookrow">
                    <td class="tablecell" colspan="2">
                        <div class="booksinglebox">
                            <h2>Lexical Dispersion Plot of TOP-10 words for {title}</h2>
                            <img width="85%" height="85%" style="" src="{{{{ url_for('static', filename='output/dispersion/{title}.png') }}}}">
                        </div>
                    </td>
                </tr>
                <tr class="bookrow">
                    <td class="tablecell" colspan="2">
                        <div class="booksinglebox">
                            <h2>Lexical Dispersion Plot of TOP-10 female names for {title}</h2>
                            <img width="85%" height="85%" style="" src="{{{{ url_for('static', filename='output/femalenames/{title}.png') }}}}">
                        </div>
                    </td>
                </tr>
                <tr class="bookrow">
                    <td class="tablecell" colspan="2">
                        <div class="booksinglebox">
                            <h2>Lexical Dispersion Plot of TOP-10 male names for {title}</h2>
                            <img width="85%" height="85%" style="" src="{{{{ url_for('static', filename='output/malenames/{title}.png') }}}}">
                        </div>
                    </td>
                </tr>
            </table>
        </body>
    </html>"""


def category_page(category):
    """
    Generates a webpage for the category
    Compatible with flask template system
    """
    start_page = f"""
    <!-- Sultanov Andriy -->
    <!-- MIT License 2020 -->
    <html>
        <head>
            <meta charset="utf-8">
            <link rel="stylesheet" type="text/css" href="{{{{ url_for('static', filename='css/style.css') }}}}">
            <link rel="shortcut icon" type="image/png" href="{{{{ url_for('static', filename='css/style.css') }}}}"/>
            <title>{category.name}</title>
        </head>
    
        <body class="body">
            <table class="tablecategory">
                <tr class="rowcategory">
                    <td class="categorytitle" colspan="7"> 
                        <h1 class="categorycenter">{category.name}</h1>
                    </td>
                </tr>"""

    cells = len(category.books)
    rows = (cells // 6) + 1

    for i in range(rows):
        start_page += """<tr class="animatedcategoryrow">"""
        for book in category.books[i*6:cells-(i*6)]:
            start_page += f"""<td class="tablecell">
                            <a href="https://text-analysis-ucu.herokuapp.com/title?title={book.title}">
                            <div class="categorybox">
                                <h2>{book.title}</h2>
                            </div>
                            </a>
                            </td>"""
        start_page += """</tr>"""
    start_page += """</table></body></html>"""

    return start_page


def home_page(books, authors, years, topics):
    """
    Generates a home webpage
    Compatible with flask template system
    """
    page = """
    <!-- Sultanov Andriy -->
    <!-- MIT License 2020 -->
    <html>
        <head>
            <meta charset="utf-8">
            <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/style.css') }}">
            <link rel="shortcut icon" type="image/png" href="{{ url_for('static', filename='css/favicon.png') }}"/>
            <title>Home</title>
        </head>
    
        <body class="body">
            <h1 class="title">Textual Analysis Data Visualization</h1>
            <h1 class="bytitle">Project by Andriy Sultanov</h1>
            <div class="subtitlediv">
                <table>
                    <tr>
                        <td>
                            <h1 class="subtitle">Categories</h1>
                        </td>
                        <td>
                            <div class='icon-scroll'></div>
                        </td>
                    </tr>
                </table>
            </div>
            <table class="tablecategories">
                <tr class="tablerow">
                    <td> 
                        <h1 class="category">Books</h1>
                    </td>
    """

    for book in books[:5]:
        page += f"""
                    <td class="tablecell">
                    <a href="https://text-analysis-ucu.herokuapp.com/title?title={book.title}">
                        <div class="box">
                            <h2>{book.title}</h2>
                        </div>
                    </a>
                    </td>"""

    page += """</tr>
                <tr class="tablerow">
                <td>
                    <h1 class="category"1>Authors</h1>
                </td>"""

    for author in authors[:5]:
        page += f"""<td class="tablecell">
                    <a href="https://text-analysis-ucu.herokuapp.com/category?title={author.name}">
                        <div class="box">
                            <h2>{author.name}</h2>
                        </div>
                    </a>
                    </td>"""

    page += """</tr>
                <tr class="tablerow">
                    <td>
                        <h1 class="category">Times</h1>
                    </td>"""

    for year in years[:5]:
        page += f"""
                    <td class="tablecell">
                    <a href="https://text-analysis-ucu.herokuapp.com/category?title={year.name}">
                        <div class="box">
                            <h2>{year.name}</h2>
                        </div>
                    </a>
                    </td>"""

    page += """</tr>
                <tr class="tablerow">
                    <td>
                        <h1 class="category">Topics</h1>
                    </td>
                    <td class="tablecell">
                        <div class="box">
                            <h2>Title</h2>
                        </div>
                    </td>
                    <td class="tablecell">
                        <div class="box">
                            <h2>Title</h2>
                        </div>
                    </td>
                    <td class="tablecell">
                        <div class="box">
                            <h2>Title</h2>
                        </div>
                    </td>
                    <td class="tablecell">
                        <div class="box">
                            <h2>Title</h2>
                        </div>
                    </td>
                    <td class="tablecell">
                        <div class="box">
                            <h2>Title</h2>
                        </div>
                    </td>
                </tr>
            </table>
        </body>
    </html>"""

    return page
