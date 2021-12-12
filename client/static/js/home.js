$(document).ready(() => {
    $.ajax({
        url:"http://127.0.0.1:5000/home",
        type:"GET",
        success : (data) =>{
            var movies = data["top-10"];
            var base_movies = "";
            for(var i = 0; i < movies.length; i+=1){
                if(i==0){
                    base_movies += `
                        <div class="carousel-item active">
                            <a href="${movies[i].url}">
                                <div class="item-top">
                                    <img src="${movies[i].img}" />
                                    <div id="info-movie">
                                        <p>TOP ${i+1}: ${movies[i].title}</p>
                                    </div>
                                </div>
                            </a>
                        </div>
                    `
                }else{
                    base_movies += `
                        <div class="carousel-item">
                            <a href="${movies[i].url}">
                                <div class="item-top">
                                    <img src="${movies[i].img}" />
                                    <div id="info-movie">
                                        <p>TOP ${i+1}: ${movies[i].title}</p>
                                    </div>
                                </div>
                            </a>
                        </div>
                    `
                }
            }
            $(".top-movie .carousel-inner").append(base_movies)

            movies = data["movies"];
            base_movies = "";
            for(var i = 0; i < movies.length; i+=1){
                var view = Object.values(movies[i].bar)
                view = view.reduce((a, b) => a+b, 0)
                view = view.toLocaleString()
                base_movies += `
                    <div class="col-md-3">
                        <a href="${movies[i].url}">
                            <div id ="item">
                                <img src="${movies[i].img}" />
                                <div>
                                    <p id="title">${movies[i].title}</p>
                                    <p id="view">${view} lượt xem</p>
                                </div>
                            </div>
                        </a>
                    </div>
                `
            }
            $(".movie-list #movie").append(base_movies)
        }
    });
})