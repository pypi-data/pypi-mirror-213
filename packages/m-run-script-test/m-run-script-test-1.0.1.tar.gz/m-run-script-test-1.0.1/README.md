### Run Script
Thư viện xử lý chạy các script của project mỗi khi deploy version mới, sau khi chạy xong thì lưu lại vết script đã chạy để lần sau không chạy lại nữa. 


### Cài đặt:
```bash
 $ pip3 install m-run-script
 ```

### Sử dụng:

##### Chạy các script của project:
   ```python
    from mobio.libs.run_script import MobioRunScript
    VERSION_CONFIG = {
        "every_deploy": {
            "script": [
                "PYTHONPATH=./ python3.8 -u sync_mongodb_index.py",
                "PYTHONPATH=./ python3.8 -u sync_kafka_topic.py"
            ]
        },
        "version": {
            1: ["PYTHONPATH=./ python3.8 -u scripts/script_1.py",
                "PYTHONPATH=./ python3.8 -u scripts/script_2.py"],
            2: ["PYTHONPATH=./ python3.8 -u scripts/script_3.py"]
        }
    }

    MobioRunScript().run_script_by_version(VERSION_CONFIG)

   ```
#### Log - 1.0.0
    - release sdk
    