import pathlib
import os


def write_genre_tags(genres):
    for genre in genres:
        htmlFile.write("<a href=\"#\" class=\"genre-btn black-border circle\"><span>"+genre+"</span></a>")

    # Close off section because genres are the last thing to go in
    htmlFile.write("</div></div></section>")


def place_box_image(index):

    if str(boxArtPaths[index]) == "":
        boxArtPath = DEFAULT_COVER_ART_PATH # TODO: REPLACE WITH BOX ART DEFAULT
    else:
        boxArtPath = str(boxArtPaths[index])

    htmlFile.write("<img src=\"" + boxArtPath + "\" alt=\"\" class=\"img-fluid\">")


def write_background_image_html(index):
    htmlFile.write("<section class=\"fade-disconnect-top home_banner_area"+str(index)+"\" style=\"height: 1000px\">")


def write_anime_name(index):
    htmlFile.write("<h1 class=\"anime_name\">"+animeNames[index].replace("-", " ")+"</h1>")


def write_description():
    htmlFile.write("<p>Description</p>")


def write_cover_css(index):

    if str(backgroundPaths[index]) == "":
        backgroundPath = DEFAULT_COVER_ART_PATH
    else:
        backgroundPath = str(backgroundPaths[index]).replace("\\", "/")
    cssFileForBackgrounds.write(".home_banner_area" + str(index) + " {z-index: 1;background: url(../" + backgroundPath + ") no-repeat scroll center;background-size: cover; background-image: -webkit-linear-gradient(left, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0) 20%, rgba(0,0,0,0) 80%, rgba(0,0,0,0.9) 100%), url(../" + backgroundPath + ");}")


def write_footer_and_scripts():
    htmlFile.write("<script src=\"js/jquery-3.2.1.min.js\"></script><script src=\"js/popper.js\"></script><script src=\"js/bootstrap.min.js\"></script><script src=\"js/stellar.js\"></script><script src=\"vendors/lightbox/simpleLightbox.min.js\"></script><script src=\"vendors/nice-select/js/jquery.nice-select.min.js\"></script><script src=\"vendors/isotope/imagesloaded.pkgd.min.js\"></script><script src=\"vendors/isotope/isotope-min.js\"></script><script src=\"vendors/owl-carousel/owl.carousel.min.js\"></script><script src=\"js/jquery.ajaxchimp.min.js\"></script><script src=\"vendors/counter-up/jquery.waypoints.min.js\"></script><script src=\"vendors/counter-up/jquery.counterup.js\"></script><script src=\"js/mail-script.js\"></script><script src=\"vendors/popup/jquery.magnific-popup.min.js\"></script><script src=\"js/theme.js\"></script></body></html>")


dataFilePaths = []
boxArtPaths = []
backgroundPaths = []
animeNames = []
newAnimeName = ""
DEFAULT_COVER_ART_PATH = "img\\default\\images\\absolute-duo-cover.jpg"
i = 0
for path, dirs, files in os.walk("anime\\"):
    for name in files:
        animeName = pathlib.PurePath(path, name).parts[1]  # Finds .txt, .png (box) then .jpg (cover)
        fileType = str(pathlib.PurePath(path, name))[-3:]
        if newAnimeName != animeName and newAnimeName != "":
            # We have moved to another anime
            animeNames.append(str(newAnimeName))
            # skip over any array elems to keep all data in same column (self balance)
            if len(boxArtPaths) < len(backgroundPaths) or len(boxArtPaths) < len(dataFilePaths):
                boxArtPaths.append("")
            if len(backgroundPaths) < len(boxArtPaths) or len(backgroundPaths) < len(dataFilePaths):
                backgroundPaths.append("")
            if len(dataFilePaths) < len(boxArtPaths) or len(dataFilePaths) < len(backgroundPaths):
                dataFilePaths.append("")
        newAnimeName = animeName
        if fileType == "txt":
            dataFilePaths.append(pathlib.PurePath(path, name))
        elif fileType == "png":
            boxArtPaths.append(pathlib.PurePath(path, name))
        elif fileType == "jpg":
            backgroundPaths.append(pathlib.PurePath(path, name))

# for x in range(0, len(animeNames)):
#     print(str(x) + " " + str(dataFilePaths[x]))
#     print(str(x) + " " + str(boxArtPaths[x]))
#     print(str(x) + " " + str(backgroundPaths[x]))

htmlFile = open("generated_index.html", "w+")
cssFileForBackgrounds = open("css/style.css", "a") # Append the new backgrounds - not wiping any old ones (this only works once)
# Setup
htmlFile.write("<!doctype html><html lang=\"en\"><head><!-- Required meta tags --><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\"><link rel=\"icon\" href=\"img/favicon.png\" type=\"image/png\"><title>Shoyu's Anime Anthology</title><!-- Bootstrap CSS --><link rel=\"stylesheet\" href=\"css/bootstrap.css\"><link rel=\"stylesheet\" href=\"vendors/linericon/style.css\"><link rel=\"stylesheet\" href=\"css/fonts.css\"><link rel=\"stylesheet\" href=\"vendors/owl-carousel/owl.carousel.min.css\"><link rel=\"stylesheet\" href=\"vendors/lightbox/simpleLightbox.css\"><link rel=\"stylesheet\" href=\"vendors/nice-select/css/nice-select.css\"><link rel=\"stylesheet\" href=\"vendors/animate-css/animate.css\"><link rel=\"stylesheet\" href=\"vendors/popup/magnific-popup.css\"><!-- main css --><link rel=\"stylesheet\" href=\"css/style.css\"><link rel=\"stylesheet\" href=\"css/responsive.css\"></head><body data-spy=\"scroll\" data-target=\"#mainNav\" data-offset=\"70\">")
# Header
htmlFile.write("<!--================Header Menu Area =================--><header class=\"header_area\"><div class=\"main_menu\" id=\"mainNav\"><nav class=\"navbar navbar-expand-lg navbar-light\"><div class=\"container\" style=\"color:#000\"><!-- Brand and toggle get grouped for better mobile display --><img src=\"img/logo.png\" alt=\"\" style=\"height:60px; padding-right:10px;\"><h5 style=\"margin-bottom:0px;\">Shoyu's anime anthology</h5><button class=\"navbar-toggler\" type=\"button\" data-toggle=\"collapse\" data-target=\"#navbarSupportedContent\" aria-controls=\"navbarSupportedContent\" aria-expanded=\"false\" aria-label=\"Toggle navigation\"><span class=\"icon-bar\"></span><span class=\"icon-bar\"></span><span class=\"icon-bar\"></span></button><!-- Collect the nav links, forms, and other content for toggling --><div class=\"collapse navbar-collapse offset\" id=\"navbarSupportedContent\"><ul class=\"nav navbar-nav menu_nav ml-auto\"><li class=\"nav-item active\"><a class=\"nav-link\">Home/About/Index</a></li> <li class=\"nav-item\"><a class=\"nav-link\">Level 1</a></li><li class=\"nav-item\"><a class=\"nav-link\">Level 2</a></li></ul></div> </div></nav></div></header>")


for i in range(0, len(animeNames)):
    write_background_image_html(i)
    htmlFile.write("<div class=\"section-top-border\" style=\"position:relative; left:80px; top:700px\"><div style=\"text-align: left\">")
    place_box_image(i)
    htmlFile.write("</div></div></section><section class=\"feature_area\" style=\"padding-top:10px; padding-left:450px; padding-right:10px; height:207px\"><div style=\"text-align: center; height: 100%\">")
    write_anime_name(i)
    write_description()
    htmlFile.write("<div>")
    # Get the data from the txt file
    dataFile = open(dataFilePaths[i], "r")
    line = dataFile.readline().replace("\n", "")  # Should be 'GENRES'
    genres = []
    while line != "AVG. SCORE":
        # Get all genres
        line = dataFile.readline().replace("\n", "")
        genres.append(line)
    genres.pop()  # AVG. SCORE gets thrown in for some reason
    write_genre_tags(genres)
    dataFile.close()
    # write css file for backgrounds
    write_cover_css(i)
    cssFileForBackgrounds.write(".fade-disconnect-top {background-size: cover; background-attachment: fixed; height: 350px; position: relative;}"
                                ".fade-disconnect-top:before{content: ''; position: absolute; left: 0;  right: 0; top: 0px; bottom: 925px; background: linear-gradient(to top, rgba(255, 255, 255, 0), #303030 100%); opacity: 1.0;}")

write_footer_and_scripts()
htmlFile.close()
cssFileForBackgrounds.close()

