$(function() {
    var level_1_sections = document.querySelectorAll(".body > section");
    if (level_1_sections.length == 0) level_1_sections = document.querySelectorAll(".body > div.section");

    if (level_1_sections.length > 0) {
        for (var i = 1; i < level_1_sections.length; ++ i) {
            level_1_sections[i].remove();
        }
        var section = level_1_sections[0];
        if (document.querySelector(".local-toc > ul > li > ul") == null) {
            var nwheader = document.createElement("div");
            nwheader.classList.add("page-header");

            nwheader.appendChild(section.querySelector("h1"));
            document.querySelector(".main-content").insertAdjacentElement("beforebegin", nwheader);

            document.querySelector(".local-toc").remove();
        } else {
            var page_header_list = [];
            for (var i = 0; i < section.children.length; ++ i) {
                if (section.children[i].tagName.toLowerCase() != "div") {
                    page_header_list.push(section.children[i]);
                } else {
                    if (section.children[i].tagName.toLowerCase() == "section") {
                        // break when meet the first section
                        break;
                    }
                    if (section.children[i].classList.contains("section")) {
                        break;
                    }
                }
            }
            var nwheader = document.createElement("div");
            nwheader.classList.add("page-header");
            for (var i = 0; i < page_header_list.length; ++ i) {
                nwheader.appendChild(page_header_list[i]);
            }
            document.querySelector(".main-content").insertAdjacentElement("beforebegin", nwheader);

            document.querySelector(".local-toc").replaceChild( 
                document.querySelector(".local-toc > ul > li > ul"),
                document.querySelector(".local-toc > ul")
            );
            // work with toc

            var offTop = $(".local-toc-div").offset().top - 20;
            var offMax = $(".local-toc-div").height() - $(".local-toc").height() - 20;
            $(window).resize(function() {
                offTop = $(".local-toc-div").offset().top - 20;
                offMax = $(".local-toc-div").height() - $(".local-toc").height() - 20;

                var scroll = $(window).scrollTop();
                if (scroll > offTop) $(".local-toc").css("top", Math.min(scroll - offTop, offMax));
                else $(".local-toc").css("top", 0);
            });
            $(window).scroll(function () {
                var scroll = $(window).scrollTop();
                if (scroll > offTop) $(".local-toc").css("top", Math.min(scroll - offTop, offMax));
                else $(".local-toc").css("top", 0);
            });
        }
    } else {
        document.querySelector(".local-toc").remove();

        if (document.querySelector(".highlight") != null) {
            document.querySelector(".highlight").classList.add("view-source");
        }
    }
});