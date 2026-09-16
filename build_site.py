#!/usr/bin/env python3
"""Build the dependency-light static BOSIO/BoAYo documentation site."""
from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup


ROOT = Path(__file__).resolve().parent
BASE_URL = "https://varzero.github.io/bosio_boayo_docs/"
PAGES = [
    ("index", "시작", "전체 소개", "BOSIO × BoAYo", "정이십면체 프레임버퍼부터 구면 데스크톱까지, 실제 구현을 한곳에서 읽습니다.", "개요 구조 저장소"),
    ("quickstart", "시작", "빠른 시작", "PYNQ-Z2 실행", "통합 저장소를 내려받고 보드에 올린 뒤 출력과 창을 확인합니다.", "설치 실행 SSH"),
    ("architecture", "시작", "시스템 구조", "세 계층의 연결", "센서, FPGA 출력 코어, Bosio 창 관리자와 BoAYo 앱의 책임을 나눕니다.", "하드웨어 소프트웨어 데이터 흐름"),
    ("geometry", "핵심 시스템", "정이십면체 장면", "20면 · 211타일 · M×M 셀", "7·7·7·8 분할과 작은 삼각 셀의 주소 체계를 설명합니다.", "정이십면체 7-7-7-8 타일 M16"),
    ("output-core", "핵심 시스템", "출력 코어 RTL", "투영과 HDMI 출력", "FPGA가 실제로 수행하는 면 선택, 자세 계수, 캐시와 영상을 설명합니다.", "RTL Q24 HDMI 센서 AXI"),
    ("sensor-buttons", "핵심 시스템", "센서와 버튼", "GY-521 · Pmod B · BTN", "직접 AXI4-Stream 센서 경로와 PYNQ 버튼 입력을 설명합니다.", "MPU6050 I2C 버튼 시선"),
    ("window-manager", "핵심 시스템", "Bosio 창 관리자", "구면 창과 부분 갱신", "창 입력과 포커스, C++/NEON 합성, 바뀐 타일만 보내는 BPT1 갱신을 설명합니다.", "IPC 합성 포커스 NEON BPT1"),
    ("external-input", "핵심 시스템", "외부 포인터 입력", "추적기와 제스처 연결", "관성 추적기·카메라 손동작 인식기 같은 별도 입력 프로세스를 구면 포인터에 연결합니다.", "입력 API 포인터 클릭 드래그 제스처 카메라 IMU"),
    ("boayo", "앱과 UI", "BoAYo 데스크톱", "패널과 앱 캡션", "런처 패널, 독립 앱 창, 클릭·드래그·닫기 규칙을 정리합니다.", "런처 패널 캡션 BTN2 앱"),
    ("sdk", "앱과 UI", "앱 SDK", "내 앱에 구면 창 붙이기", "BoayoSDK로 내용을 그리고 이벤트를 받는 앱 예제를 제공합니다.", "BoayoSDK Python API 예제"),
    ("sdk-reference", "앱과 UI", "SDK 함수·이벤트", "함수와 이벤트 안내", "창 만들기와 닫기, 공개 함수, 상태값과 이벤트의 사용법을 찾아봅니다.", "SDK API 함수 이벤트 BoayoEvent BoayoWindowState Surface"),
    ("deployment", "운영", "배포와 부팅", "FullStack 실행 절차", "세 저장소와 통합 저장소, 자동 시작 서비스 및 업데이트 흐름입니다.", "FullStack GitHub 부팅 서비스 배포"),
    ("quality", "운영", "화질과 성능", "AA · 해상도 · 검증", "M=16의 화질 한계, 두 단계 AA와 실제 확인 지표를 구분합니다.", "AA FPS 성능 투영 RGB332"),
    ("reference", "참고", "데이터와 소스", "데이터 형식과 원본 코드", "센서·앱·장면 데이터의 형식과 전달 경로, 개발 저장소를 정리했습니다.", "데이터 형식 저장소 레지스터 API"),
]


def main():
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("page.html")
    for slug, group, label, title, summary, keywords in PAGES:
        source = ROOT / "content" / f"{slug}.html"
        if not source.is_file():
            raise SystemExit(f"missing documentation content: {source}")
        output = ROOT / f"{slug}.html"
        output.write_text(
            template.render(
                slug=slug, group=group, label=label, title=title,
                summary=summary, keywords=keywords, pages=PAGES,
                content=Markup(source.read_text(encoding="utf-8")),
                canonical=BASE_URL + ("" if slug == "index" else f"{slug}.html"),
            ),
            encoding="utf-8",
        )
    (ROOT / "assets" / "search-index.json").write_text(
        json.dumps([
            {"url": "./" if slug == "index" else f"{slug}.html", "label": label,
             "title": title, "summary": summary, "keywords": keywords}
            for slug, _, label, title, summary, keywords in PAGES
        ], ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{escape(BASE_URL + ('' if slug == 'index' else slug + '.html'))}</loc></url>\n"
                for slug, *_ in PAGES) + "</urlset>\n", encoding="utf-8",
    )
    print(f"built {len(PAGES)} documentation pages")


if __name__ == "__main__":
    main()
