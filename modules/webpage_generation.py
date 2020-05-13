def bookpage(title, wordcolor):
    return f"""
    <html>
        <head>
            <meta charset="utf-8">
            <link rel="stylesheet" type="text/css" href="../style.css">
            <link rel="shortcut icon" type="image/png" href="favicon.png"/>
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
                            <img width="82%" height="82%" src="../../../output/wordclouds/{title}.jpg">
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
                            <img width="85%" height="85%" style="" src="../../../output/dispersion/{title}.png">
                        </div>
                    </td>
                </tr>
                <tr class="bookrow">
                    <td class="tablecell" colspan="2">
                        <div class="booksinglebox">
                            <h2>Lexical Dispersion Plot of TOP-10 female names for {title}</h2>
                            <img width="85%" height="85%" style="" src="../../../output/femalenames/{title}.png">
                        </div>
                    </td>
                </tr>
                <tr class="bookrow">
                    <td class="tablecell" colspan="2">
                        <div class="booksinglebox">
                            <h2>Lexical Dispersion Plot of TOP-10 male names for {title}</h2>
                            <img width="85%" height="85%" style="" src="../../../output/malenames/{title}.png">
                        </div>
                    </td>
                </tr>
            </table>
        </body>
    </html>"""


def category_page(category):
    start_page = f"""
    <!-- Sultanov Andriy -->
    <!-- MIT License 2020 -->
    <html>
        <head>
            <meta charset="utf-8">
            <link rel="stylesheet" type="text/css" href="../style.css">
            <link rel="shortcut icon" type="image/png" href="favicon.png"/>
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
                            <div class="categorybox">
                            <a href="https://website.com/?title={book.title}">
                                <h2>{book.title}</h2>
                            </a>
                            </div>
                            </td>"""
        start_page += """</tr>"""
    start_page += """</table></body></html>"""

    return start_page