import requests

def get_random_quote():
    """
    دریافت یک جمله تصادفی از API بدون نیاز به کلید
    خروجی: (content, author)
    """
    try:
        url = "https://api.quotable.io/random"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return (data.get('content'), data.get('author'))
        else:
            return None
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

def get_quote_by_tag(tag):
    """
    دریافت جمله بر اساس موضوع (مثلاً wisdom, love)
    خروجی: (content, author)
    """
    try:
        url = f"https://api.quotable.io/random?tags={tag}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return (data.get('content'), data.get('author'))
        else:
            return None
    except Exception as e:
        print(f"Connection Error: {e}")
        return None
    
if __name__ == "__main__":
    print("در حال دریافت یک جمله تصادفی...")
result = get_random_quote()
if result:
    print(f"جمله: {result[0]}")
    print(f"نویسنده: {result[1]}")
else:
    print("خطا در دریافت اطلاعات. احتمالاً VPN خاموش است.")