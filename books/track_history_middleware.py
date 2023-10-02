class TrackHistoryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # 세션에서 URL 히스토리 가져오기
        url_history = request.session.get('url_history', [])

        # 현재 URL 추가
        current_url = request.get_full_path()
        url_history.append(current_url)

        # URL 히스토리가 너무 길어지면, 앞 부분을 자름
        if len(url_history) > 10:
            url_history = url_history[-10:]

        # 세션에 URL 히스토리 업데이트
        request.session['url_history'] = url_history

        return response