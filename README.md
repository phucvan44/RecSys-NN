# Recommendation System


### Tổng quang về Recommendation System
- Recommend dựa trên đánh giá của người dùng
- Recommend dựa trên thể loại của phim

#### Recommend dựa trên đánh giá của người dùng
Dùng mạng Neural Network để đánh giá các bộ phim mà chưa được người dùng nào đánh giá. Sau đó tìm kiếm các bộ phim có đánh giá tương tự để gợi ý.
#### Recommend dựa trên thể loại của phim
Lọc ra các thể loại của phim. Sắp xếp các bộ phim có cùng nhiều thể loại với bộ phim đang xem nhất

# Thực hiện
### Yêu cầu thư viện trong Python
- sklearn
- keras
- numpy
- pandas
- json
- flask


### Tiền xử lý dữ liệu 
Chúng ta cần tiền xử lý dữ liệu để khi dùng chỉ ta chỉ cần import các module cần thiết và không cần phải mất thời gian train lại model.

Mở thư mục hiện tại và làm các bước sau:

```sh
cd model
python clean_data.py
```

### Train model
Sau khi chúng ta đã xử lí các dữ liệu cần thiết. Bây giờ chúng ta sẽ train model
Ta tiếp tục thực hiện như sau:

```sh
python train_model.py
```

### Predict model
Bước cuối cùng là predict model. Bước này sẽ thực hiện dự đoán các rating mà chưa được người dùng đánh giá. Thực hiện lọc các neighbors bằng rating và genres .Tạo ra các file JSON để thuận tiện việc call API.
Ta tiếp tục thực hiện như sau:
```sh
python predict_model.py
```

### Chạy Server Python Flask
```sh
cd ../server
set FLASK_APP=main.py
flask run
```

### Chạy Client
Vào thư mục ./client và mở file index.html.
