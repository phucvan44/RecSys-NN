$(document).ready(() => {
    var get_parameters = () => {
        let url = window.location.search.substring(1);
        url = url.split("&")
        let params = {}
        url.forEach(str => {
            str = str.split("=")
            params[str[0]] = str[1]
        });
        return params
    }
    
    var params = get_parameters()
    if("id" in params){
        $.ajax({
            url:"http://127.0.0.1:5000/movies/detail/"+(params["id"]-1),
            type:"GET",
            success : (data) =>{
                var movie = data["movie"];
                $(".movie-detail #img-movie").attr("src", movie["img"])
                $(".movie-detail #detail h1").text(movie["title"])

                var view = Object.values(movie["bar"])
                view = view.reduce((a, b) => a+b, 0)
                view = view.toLocaleString()

                $(".movie-detail #detail #_view").text(view)
                
                var viewbar = Object.values(movie["bar"])
                var fl = false;
                for(var i = 1; i <viewbar.length; i+=1){
                    viewbar[i] = (viewbar[i]/10) + 10;
                    if(viewbar[i] > 100){
                        fl = true;
                    }
                }
                if(fl){
                    for(var i = 1; i <viewbar.length; i+=1){
                        viewbar[i] = viewbar[i]/2 + 3;
                    }
                }
                view = Object.values(movie["bar"]);
                var bar = `
                    <div id="0.5" class="_bar_" style="height: ${viewbar[1]}px;">
                        <div id="sub-title">
                            <h4>0.5</h4>
                            <p>${view[1]} votes</p>
                        </div>
                    </div>
                    <div id="1.0" class="_bar_" style="height: ${viewbar[2]}px;">
                        <div id="sub-title">
                            <h4>1.0</h4>
                            <p>${view[2]} votes</p>
                        </div>
                    </div>
                    <div id="1.5" class="_bar_" style="height: ${viewbar[3]}px;">
                        <div id="sub-title">
                            <h4>1.5</h4>
                            <p>${view[3]} votes</p>
                        </div>
                    </div>
                    <div id="2.0" class="_bar_" style="height: ${viewbar[4]}px;">
                        <div id="sub-title">
                            <h4>2.0</h4>
                            <p>${view[4]} votes</p>
                        </div>
                    </div>
                    <div id="2.5" class="_bar_" style="height: ${viewbar[5]}px;">
                        <div id="sub-title">
                            <h4>2.5</h4>
                            <p>${view[5]} votes</p>
                        </div>
                    </div>
                    <div id="3.0" class="_bar_" style="height: ${viewbar[6]}px;">
                        <div id="sub-title">
                            <h4>3.0</h4>
                            <p>${view[6]} votes</p>
                        </div>
                    </div>
                    <div id="3.5" class="_bar_" style="height: ${viewbar[7]}px;">
                        <div id="sub-title">
                            <h4>3.5</h4>
                            <p>${view[7]} votes</p>
                        </div>
                    </div>
                    <div id="4.0" class="_bar_" style="height: ${viewbar[8]}px;">
                        <div id="sub-title">
                            <h4>4.0</h4>
                            <p>${view[8]} votes</p>
                        </div>
                    </div>
                    <div id="4.5" class="_bar_" style="height: ${viewbar[9]}px;">
                        <div id="sub-title">
                            <h4>4.5</h4>
                            <p>${view[9]} votes</p>
                        </div>
                    </div>
                    <div id="5.0" class="_bar_" style="height: ${viewbar[10]}px;">
                        <div id="sub-title">
                            <h4>5.0</h4>
                            <p>${view[10]} votes</p>
                        </div>
                    </div>
                `
                $(".movie-detail #detail #rating-bar").append(bar)
            
                var genres = ""
                for(var i = 0; i < movie.genres.length; i+=1){
                    genres += `
                        <li>
                            <a href="${movie.genres[i].url}"><button>${movie.genres[i].value}</button></a>
                        </li>
                    `
                }

                $(".movie-detail #genre ul").append(genres);

                var neighbors_rating = "";
                var neighbors_genres = "";
                for(var i = 0; i < data.neighbors_rating.length; i+=1){
                    view = Object.values(data.neighbors_tag[i].bar)
                    view = view.reduce((a, b) => a+b, 0)
                    view = view.toLocaleString()

                    neighbors_genres += `
                        <div class="col-md-3">
                            <a href="${data.neighbors_tag[i].url}">
                                <div id ="item">
                                    <img src="${data.neighbors_tag[i].img}" />
                                    <div>
                                        <p id="title">${data.neighbors_tag[i].title}</p>
                                        <p id="view">${view} lượt xem</p>
                                    </div>  
                                </div>
                            </a>
                        </div>
                    `
                    view = Object.values(data.neighbors_rating[i].bar)
                    view = view.reduce((a, b) => a+b, 0)
                    view = view.toLocaleString()

                    neighbors_rating += `
                        <div class="col-md-3">
                            <a href="${data.neighbors_rating[i].url}">
                                <div id ="item">
                                    <img src="${data.neighbors_rating[i].img}" />
                                    <div>
                                        <p id="title">${data.neighbors_rating[i].title}</p>
                                        <p id="view">${view} lượt xem</p>
                                    </div>  
                                </div>
                            </a>
                        </div>
                    `
                }
                $("._rec-rating").append(neighbors_rating);
                $("._rec-genres").append(neighbors_genres);
            }
        });
    }

})