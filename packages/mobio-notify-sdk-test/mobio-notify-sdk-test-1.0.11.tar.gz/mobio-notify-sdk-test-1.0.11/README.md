## Cài đặt thư viện SDK Notify

### Sừ dụng:

- Link lấy thông tin field mapping template chuẩn hoá Notify-SDK: https://docs.google.com/spreadsheets/d/1qPD_ovHt_p9HL5P9K8XOgeJjFGeduKVdM6ImmXuJo0c/edit?usp=sharing
#### 1. Khởi tạo SDK:

```python
from mobio.sdks.notify import MobioNotifySDK

# Khởi tạo cấu hình chung SDK
MobioNotifySDK().config(
    source=""  # source module (nguồn gửi từ module nào) (Ex: 'sale', 'admin')
)

```

#### 2.Gửi thông báo toàn kênh ( Mobile App, Browser, Web(in-app), Email )

```python
"""
    Gửi thông báo toàn kênh
    :param merchant_id: Id thương hiệu
    :param key_config: kiểu thông báo (được cấu hình trên admin) (ex: 'jb_create_by_me_end',
    'jb_estimate_target_size')
    :param account_ids: Danh sách id nhân viên (id nhân viên của module ADMIN) (Nếu không truyền lên sẽ mặc định
    lấy những ID nhân viên nào bật cấu hình thông báo)
    :param kwargs: Thông tin các field nội dung thông báo toàn kênh định dạng key=value
    Truyền định dạng send_message_notify(merchant_id, key_config, account_ids, deal_count=5) lên hàm xử lý.
    SDK sẽ tự bắt thông tin field để thực hiện replace theo nội dung đã được cấu hình trên Admin.
    EX: title: Thông báo đơn hàng tồn quá **deal_count** đơn.
        content: Thông báo đơn hàng tồn quá **deal_count** đơn.
                Vui lòng phân công cho nhân viên xử lý.
    - Field chuẩn hoá gửi kênh email truyền thêm các field sau(vì là kwargs vui lòng truyền đúng định dạng key=value):
        + email_sender_name: "" Tên người gửi/ nguồn gửi (VD: default: 'Mobio Alert')
        + email_file_alert: boolean (Cấu hình nút tải file/ xem chi tiết (không bắt buộc), custom nội dung thông báo bắt buộc gửi
        email_file_alert=False(có button) và ngược lại bằng True thì sẽ không có)
        + email_button_name: string (Tên button email, mặc định ko truyền lên filed này sẽ có giá trị = "Tải file",
                                    email_file_alert = True bỏ qua field này)
        + email_url_file: string (đường dẫn khi submit vào button email; email_file_alert = True bỏ qua field này)
        + email_subject: string (nếu muốn tự custom tiêu đề email)
        + email_content: string (nếu muốn tự custom nội dung email)
        + other_emails: thông tin danh sách email muốn gửi thêm ngoài thông tin account_ids (
        là một list string email, ex: ["luongnd@mobio.io", "luongtest@gmail.com"])
    - Field chuẩn hoá gửi kênh socket truyền thêm các field sau (vì là kwargs vui lòng truyền đúng định dạng key=value):
        + socket_title: string (Nếu muốn tự custom tiêu đề gửi đến các kênh App, Browser, Web)
        + socket_content: string (Nếu muốn tự custom nội dung gửi đến các kênh App, Browser, Web)
    '''
     EX:
        + Gửi thông báo "Thông báo bạn được phân công cuộc hội thoại mới"
        - Nội dung email:
            - email_subject: Bạn có một cuộc hội thoại mới
            - email_content: Bạn có một cuộc hội thoại mới **conversation_name** vào **time** trước
        - Nội dung kênh socket(app, mobile, browser):
            - socket_title: Bạn có cuộc hội thoại mới
            - socket_content: Bạn có một cuộc hội thoại mới **conversation_name** vào **time** trước
    '''
"""

MobioNotifySDK().send_message_notify(
    merchant_id="", key_config="",
    account_ids=["uuid1", "uuid2"],
    conversation_name="",  # field trong kwargs
    time=""  # field trong kwargs
)
```

#### 3. Gửi thông báo socket đến các kênh Mobile App, Browser, Web(In-app)

```python
"""
:param merchant_id: ID thương hiệu cần gửi thông báo
    :param key_config: kiểu thông báo (được cấu hình trên admin) (ex: 'jb_create_by_me_end',
    'jb_estimate_target_size')
    :param account_ids: Danh sách id nhân viên (id nhân viên của module ADMIN) (Nếu không truyền lên sẽ mặc định
    lấy những ID nhân viên nào bật cấu hình thông báo)
    :param kwargs: Thông tin các field nội dung thông báo toàn kênh định dạng key=value
    Truyền định dạng send_message_notify_socket(merchant_id, key_config, account_ids, deal_count=5) lên hàm xử lý.
    SDK sẽ tự bắt thông tin field để thực hiện replace theo nội dung đã được cấu hình trên Admin.
    EX: title: Thông báo đơn hàng tồn quá **deal_count** đơn.
        content: Thông báo đơn hàng tồn quá **deal_count** đơn.
                Vui lòng phân công cho nhân viên xử lý.
    
    - Field chuẩn hoá gửi kênh socket truyền thêm các field sau (vì là kwargs vui lòng truyền đúng định dạng key=value):
        + title: string (Nếu muốn tự custom tiêu đề gửi đến các kênh App, Browser, Web)
        + content: string (Nếu muốn tự custom nội dung gửi đến các kênh App, Browser, Web)
"""


MobioNotifySDK().send_message_notify_socket(
    merchant_id="", key_config="",
    account_ids=["uuid1", "uuid2"],
    conversation_name="",  # field trong kwargs
    time=""  # field trong kwargs
)

# Tự custom nội dung thông báo
MobioNotifySDK().send_message_notify_socket(
    merchant_id="", key_config="",
    account_ids=["uuid1", "uuid2"],
    conversation_name="",  # field trong kwargs
    time="",  # field trong kwargs
    title="Test gửi thông báo",
    content="Nội dung thông báo"
)

```

#### 4. Gửi email thông báo

```python
"""
    Hàm thực hiện việc gửi email thông báo
    
    :param merchant_id: ID thương hiệu cần gửi thông báo
    :param key_config: kiểu thông báo (được cấu hình trên admin) (ex: 'jb_create_by_me_end',
    'jb_estimate_target_size')
    :param account_ids: Danh sách id nhân viên (id nhân viên của module ADMIN) (Nếu không truyền lên sẽ mặc định
    lấy những ID nhân viên nào bật cấu hình thông báo)
    :param kwargs: Thông tin các field nội dung thông báo toàn kênh định dạng key=value
    Truyền định dạng send_message_notify_email(merchant_id, key_config, account_ids, deal_count=5) lên hàm xử lý.
    SDK sẽ tự bắt thông tin field để thực hiện replace theo nội dung đã được cấu hình trên Admin.
    EX: title: Thông báo đơn hàng tồn quá **deal_count** đơn.
        content: Thông báo đơn hàng tồn quá **deal_count** đơn.
                Vui lòng phân công cho nhân viên xử lý.
    - Field chuẩn hoá gửi kênh email truyền thêm các field sau(vì là kwargs
        vui lòng truyền đúng định dạng key=value):
        + sender_name: "Tên người gửi/ nguồn gửi (VD: default: 'Mobio Alert')"
        + file_alert: boolean (Cấu hình nút tải file/ xem chi tiết (không bắt buộc), custom nội dung thông báo bắt buộc gửi
            file_alert=False(có button) và ngược lại bằng True thì sẽ không có)
        + button_name: string (Tên button email, mặc định ko truyền lên filed này sẽ có giá trị = "Tải file",
                                    email_file_alert = True bỏ qua field này)
        + url_file: string (đường dẫn khi submit vào button email; email_file_alert = True bỏ qua field này)
        + subject: string (nếu muốn tự custom tiêu đề email)
        + content: string html (nếu muốn tự custom nội dung email) (chỉ là nội dung bên trong,
         không chưa cả khung template)
        + other_emails: thông tin danh sách email muốn gửi thêm ngoài thông tin account_ids (
        là một list string email, ex: ["luongnd@mobio.io", "luongtest@gmail.com"])
"""

MobioNotifySDK().send_message_notify_email(
    merchant_id="", key_config="",
    account_ids=["uuid1", "uuid2"],
    email_file_alert=False,
    conversation_name="",  # field trong kwargs
    time=""  # field trong kwargs
)

# Tự custom nội dung thông báo
MobioNotifySDK().send_message_notify_email(
    merchant_id="", key_config="",
    account_ids=["uuid1", "uuid2"],
    conversation_name="",  # field trong kwargs
    time="",  # field trong kwargs
    subject="Test gửi thông báo",
    content="<p>Nội dung thông báo</p>"
)
```

#### 5. Gửi thông báo Mobile App qua đầu Push ID (Firebase Notification)

```python
"""
:param merchant_id: ID thương hiệu cần gửi thông báo
:param key_config: kiểu thông báo (được cấu hình trên admin) (ex: 'jb_create_by_me_end',
'jb_estimate_target_size')
:param account_ids: Danh sách id nhân viên (id nhân viên của module ADMIN) (Nếu không truyền lên sẽ mặc định
lấy những ID nhân viên nào bật cấu hình thông báo)
:param kwargs: Thông tin các field nội dung thông báo toàn kênh định dạng key=value
Truyền định dạng send_message_notify_push_id_mobile_app(merchant_id, key_config, account_ids, deal_count=5) lên hàm xử lý.
SDK sẽ tự bắt thông tin field để thực hiện replace theo nội dung đã được cấu hình trên Admin.
EX: title: Thông báo đơn hàng tồn quá **deal_count** đơn.
    content: Thông báo đơn hàng tồn quá **deal_count** đơn.
            Vui lòng phân công cho nhân viên xử lý.

- Field chuẩn hoá gửi kênh push_id mobile app truyền thêm các field sau (vì là kwargs vui lòng truyền đúng định dạng key=value):
    + title: string (Nếu muốn tự custom tiêu đề gửi)
    + content: string (Nếu muốn tự custom nội dung gửi)
"""

MobioNotifySDK().send_message_notify_push_id_mobile_app(
    merchant_id="", key_config="",
    account_ids=["uuid1", "uuid2"],
    conversation_name="",  # field trong kwargs
    time=""  # field trong kwargs
)

# Tự custom nội dung thông báo
MobioNotifySDK().send_message_notify_push_id_mobile_app(
    merchant_id="", key_config="",
    account_ids=["uuid1", "uuid2"],
    conversation_name="",  # field trong kwargs
    time="",  # field trong kwargs
    title="Test gửi thông báo",
    content="Nội dung thông báo"
)
```

#### 6. Một số gợi ý nhỏ về việc gửi danh sách giá trị *kwargs
```python
'''
Nếu trường hợp có nhiều field gía trị để truyền vào **kwargs ta có thể dùng cách sau
để rút gọn việc đẩy các gía trị vào hàm gửi thông báo giúp clear code hơn

EX: Gửi thông báo đơn hàng mới.
    - Gửi thông tin thông báo có thể phải gửi thêm cả các thông tin như: ID nhân viên phân công,
     tên đơn hàng, ID quy trình bán ....
)
'''

# Cách chưa rút gọn
MobioNotifySDK().send_message_notify_push_id_mobile_app(
    merchant_id="", key_config="sale_add_deal",
    account_ids=["uuid1", "uuid2"],
    assignee_id="",  # field trong kwargs
    deal_name="",  # field trong kwargs
    sale_process_id=""
)

# Cách rút gọn
deal_info = {
    "assignee_id": "",
    "deal_name": "",
    "sale_process_id": "",
    "created_time": ""
}
MobioNotifySDK().send_message_notify_push_id_mobile_app(
    merchant_id="", key_config="sale_add_deal",
    account_ids=["uuid1", "uuid2"],
    **deal_info
)
```

