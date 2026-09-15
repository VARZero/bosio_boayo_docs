# BOSIO × BoAYo 문서

PYNQ-Z2의 정이십면체 프레임버퍼 출력 코어, 센서 허브, 구면 창 관리자, BoAYo 데스크톱·앱 SDK의 통합 문서입니다.

**문서 사이트:** https://varzero.github.io/bosio_boayo_docs/

문서는 `content/*.html`에 작성하고 `python build_site.py`로 저장소 루트의 정적 페이지를 생성합니다. GitHub Pages의 게시 원본은 `main` 브랜치의 `/` 루트입니다. `.nojekyll`을 포함하며 별도 서버·CDN 없이 동작합니다.

```sh
python -m pip install -r requirements.txt
python build_site.py
```

구성 요소 소스는 각각 [bosio_OutputCore](https://github.com/VARZero/bosio_OutputCore), [bosio_SphericalWM](https://github.com/VARZero/bosio_SphericalWM), [bosio_BoAYO](https://github.com/VARZero/bosio_BoAYO)에 있으며, [bosio_FullStack](https://github.com/VARZero/bosio_FullStack)이 검증된 커밋과 통합 배포 절차를 고정합니다. 소스 라이선스는 각 저장소를 따릅니다.

문서를 고칠 때는 원본 구현을 확인하고 `content`를 수정한 뒤 생성된 HTML·검색 색인·sitemap도 함께 커밋하세요.
