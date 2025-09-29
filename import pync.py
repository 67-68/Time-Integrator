import pync

def send_simple_notification():
    try:
        pync.notify(
            '这是标题：挑战时间！',
            title='Time Integrator',
            subtitle='来自你的干涉系统',
            # 你甚至可以加上一个点击后打开URL的动作
            open='https://www.google.com' 
        )
        print("Notification sent successfully!")
    except Exception as e:
        # 在某些环境下pync可能没有权限，需要错误处理
        print(f"Failed to send notification: {e}")

# 调用它
send_simple_notification()