// For Aladin Book API and input controls

var results;	// global book search results

function unescapeHTML(html) {
   var htmlNode = document.createElement("div");
   htmlNode.innerHTML = html;
   if(htmlNode.innerText !== undefined)
      return htmlNode.innerText; // IE
   return htmlNode.textContent; // FF
}

var obj = {

	apikey: "ttbncc17012351008",
	init : function()
	{
		obj.q = document.getElementById('q');
		obj.b = document.getElementById('b');
		obj.r = document.getElementById('r');
		if (obj.b != null) obj.b.onclick = obj.pingSearch;
	},

	pingSearch : function() 
	{
		if (obj.q.value) 
		{
			obj.s = document.createElement('script');
			obj.s.type ='text/javascript';
			obj.s.charset ='utf-8';
			obj.s.src = 'https://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey=' + obj.apikey + 
			'&QueryType=Keyword&MaxResults=10&start=1&SearchTarget=Book&CallBack=obj.pongSearch&output=JS&Version=20070901&Query=' + encodeURI(obj.q.value);
			document.getElementsByTagName('head')[0].appendChild(obj.s);
		}
	},

	pongSearch : function(b, z)
	{
		obj.r.innerHTML = '';
		var cards = document.createElement('div');
		cards.setAttribute("class", "container");
		for (var i = 0; i < z.item.length; i++)
		{
			var cardDiv = document.createElement('div');
			cardDiv.setAttribute("class", "book_result row");
            {
                var imgDiv = document.createElement("div");
                imgDiv.setAttribute("class", "col-3")
                {
                    if (z.item[i].cover != null)
                    {
                        var img = document.createElement('img');
                        img.src = z.item[i].cover;
                        img.setAttribute("class", "img-fluid shadow");
                        imgDiv.appendChild(img);
                    }
                    imgDiv.innerHTML += "<br/>";
                    var button = document.createElement('button');
                    button.setAttribute("class", "btn btn-outline-secondary mt-1");
                    {
                        button.setAttribute("onClick", "javascript:obj.selectbook("+i+");");
                        button.innerHTML = "<i class='material-icons'>create</i>";
                    }
                    imgDiv.appendChild(button);
                }
                cardDiv.appendChild(imgDiv);

                var textDiv = document.createElement("div");
                textDiv.setAttribute("class", "book_contents col-9");
                {
                    var contents = document.createElement("p");
                    {
                        contents.innerHTML += unescapeHTML(z.item[i].author);
                        contents.innerHTML += "<br/>";
                        contents.innerHTML += "<b>" + unescapeHTML(z.item[i].title) + "</b>";
                        contents.innerHTML += "<br/>";
                        contents.innerHTML += unescapeHTML(z.item[i].publisher);
                        contents.innerHTML += "<br/>";
                    }
                    textDiv.appendChild(contents);
                }
                cardDiv.appendChild(textDiv);
            }
			cards.appendChild(cardDiv);
		}
		obj.r.appendChild(cards);
		results = z;
	},

	fillinput  : function(i) {
		var input = document.getElementById("id_title");
		var value = results.item[i].title;
		value = unescapeHTML(value);
		value = value.replace(/<\/?[^>]+(>|$)/g, "");
		input.value = value;
		
		input = document.getElementById("id_isbn");
		value = results.item[i].isbn13;
		value = unescapeHTML(value);
		value = value.replace(/<\/?[^>]+(>|$)/g, "");
		input.value = value;
		
		var author = results.item[i].author;
		author = unescapeHTML(author);
		author = author.replace(/<\/?[^>]+(>|$)/g, ""); // Remove any tag
		author = author.replace(/지음/g, "");
		author = author.replace(/옮김/g, "");
		author = author.replace(/ 외 /g, "");
		author = author.replace(/[.,]/g, "");
		document.getElementById("id_author").value = author;
		
		var cat = results.item[i].categoryName;
		cat = cat.replace(/>/g, " "); // "인문학 > 서양철학 > 근대철학"
		cat = cat.trim().split(" ").slice(-1);

		var publisher = results.item[i].publisher;
		publisher = unescapeHTML(publisher);
		publisher = publisher.replace(/<\/?[^>]+(>|$)/g, ""); // Remove any tag
		document.getElementById("id_publisher").value = publisher;
		
		var tags = document.getElementById("id_tags");
		author = author.replace(/[A-Z]/g, ""); // Remove english author name
		author = author.trim();
		if (author.search(cat) < 0)
		    tags.value = author + " " + cat;
		else
		    tags.value = author;
		tags.focus();

		var link = document.getElementById("link");
		link.value = results.item[i].link;

		var imageLink = document.getElementById("imageLink");
		imageLink.value = results.item[i].cover;
	},
	
	selectbook : function(i) {
	    obj.check_isbn(i);
		// obj.fillinput(i);
	},

	check_isbn : function(i) {
		var isbn = results.item[i].isbn13;
		if (isbn != null)
		{
		console.log(isbn);
			$.ajax({
			url: "/checkisbn?isbn=" + isbn,
			dataType: "json",
			success: function(data) {
			    console.log(data);
				if (data.checkisbn == true) {
					window.location = "/save?isbn=" + isbn;
				} else {
					obj.fillinput(i);
				}				
			},
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('error: ', jqXHR, textStatus, errorThrown); // 에러 정보를 콘솔에 출력
                obj.fillinput(i);
            },
			fail:function(){
			    console.log("fail");
				obj.fillinput(i); 
			}});
		}
	},

};

$(window).on('load', function() {
	obj.init();
})
