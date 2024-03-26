使用py-playwright访问bilibili并清理长时间未更新的关注up主的脚本



    mkdir doubao-playwright
    cd doubao-playwright/
    python3 -m venv .venv
    source .venv/bin/activate
    
    playwright install
    
    playwright install-deps


playwright codegen  https://www.bilibili.com/ --save-storage=auth.json


playwright codegen --load-storage=auth.json  https://space.bilibili.com/750367/fans/follow
