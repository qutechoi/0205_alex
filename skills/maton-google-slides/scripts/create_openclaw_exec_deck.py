#!/usr/bin/env python3
"""Create a 5-slide executive-style OpenClaw intro deck via Maton Google Slides API."""
import argparse
from pathlib import Path
import requests

EMU = 914400
NAVY = {'red': 0.0, 'green': 0.12156863, 'blue': 0.24705882}  # #001F3F
WHITE = {'red': 1.0, 'green': 1.0, 'blue': 1.0}
GOLD = {'red': 0.86, 'green': 0.74, 'blue': 0.45}
SKY = {'red': 0.47, 'green': 0.78, 'blue': 0.95}


def build_requests():
    left = int(0.55 * EMU)
    width = int(9.3 * EMU)
    card_top = int(1.35 * EMU)
    card_height = int(3.9 * EMU)

    requests_list = []

    # Remove default auto slide if exists
    requests_list.append({'deleteObject': {'objectId': 'p'}})

    # Set background for slides
    for sid in ['slide1', 'slide2', 'slide3', 'slide4', 'slide5']:
        requests_list.append({
            'updatePageProperties': {
                'objectId': sid,
                'pageProperties': {
                    'pageBackgroundFill': {
                        'solidFill': {
                            'color': {'rgbColor': NAVY}
                        }
                    }
                },
                'fields': 'pageBackgroundFill.solidFill.color'
            }
        })

    font_family = 'Pretendard'

    # Title/subtitle slide
    requests_list.append({
        'updateTextStyle': {
            'objectId': 's1_title',
            'textRange': {'type': 'ALL'},
            'style': {
                'fontFamily': font_family,
                'fontSize': {'magnitude': 44, 'unit': 'PT'},
                'bold': True,
                'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}
            },
            'fields': 'fontFamily,fontSize,bold,foregroundColor'
        }
    })
    requests_list.append({
        'updateTextStyle': {
            'objectId': 's1_sub',
            'textRange': {'type': 'ALL'},
            'style': {
                'fontFamily': font_family,
                'fontSize': {'magnitude': 22, 'unit': 'PT'},
                'bold': False,
                'foregroundColor': {'opaqueColor': {'rgbColor': SKY}}
            },
            'fields': 'fontFamily,fontSize,bold,foregroundColor'
        }
    })

    # Body slides
    for i in range(2, 6):
        title_id = f's{i}_title'
        body_id = f's{i}_body'
        card_id = f's{i}_card'
        slide_id = f'slide{i}'

        # Glassmorphism card
        requests_list.append({
            'createShape': {
                'objectId': card_id,
                'shapeType': 'ROUND_RECTANGLE',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'width': {'magnitude': width, 'unit': 'EMU'},
                        'height': {'magnitude': card_height, 'unit': 'EMU'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': left,
                        'translateY': card_top,
                        'unit': 'EMU'
                    }
                }
            }
        })
        requests_list.append({
            'updateShapeProperties': {
                'objectId': card_id,
                'shapeProperties': {
                    'shapeBackgroundFill': {
                        'solidFill': {
                            'color': {'rgbColor': WHITE},
                            'alpha': 0.08
                        }
                    },
                    'outline': {'propertyState': 'NOT_RENDERED'}
                },
                'fields': 'shapeBackgroundFill.solidFill.color,shapeBackgroundFill.solidFill.alpha,outline.propertyState'
            }
        })

        # Title style
        requests_list.append({
            'updateTextStyle': {
                'objectId': title_id,
                'textRange': {'type': 'ALL'},
                'style': {
                    'fontFamily': font_family,
                    'fontSize': {'magnitude': 36, 'unit': 'PT'},
                    'bold': True,
                    'foregroundColor': {'opaqueColor': {'rgbColor': GOLD}}
                },
                'fields': 'fontFamily,fontSize,bold,foregroundColor'
            }
        })
        # Body style
        requests_list.append({
            'updateTextStyle': {
                'objectId': body_id,
                'textRange': {'type': 'ALL'},
                'style': {
                    'fontFamily': font_family,
                    'fontSize': {'magnitude': 20, 'unit': 'PT'},
                    'bold': False,
                    'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}
                },
                'fields': 'fontFamily,fontSize,bold,foregroundColor'
            }
        })

    return requests_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', default='OpenClaw 소개 (5장)')
    parser.add_argument('--connection-id', required=True)
    parser.add_argument('--api-key-path', required=True)
    args = parser.parse_args()

    key = Path(args.api_key_path).read_text().strip()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {key}',
        'X-Maton-Connection-Id': args.connection_id,
    }

    # Create presentation
    resp = requests.post('https://gateway.maton.ai/google-slides/v1/presentations', headers=headers, json={
        'title': args.title
    })
    resp.raise_for_status()
    prez_id = resp.json()['presentationId']

    # Create 5 slides with text boxes (IDs referenced by build_requests)
    create_requests = []

    # Slide 1
    create_requests.append({'createSlide': {'objectId': 'slide1', 'slideLayoutReference': {'predefinedLayout': 'BLANK'}}})
    create_requests.append({'createShape': {
        'objectId': 's1_title',
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': 'slide1',
            'size': {'width': {'magnitude': int(9.3*EMU), 'unit': 'EMU'}, 'height': {'magnitude': int(0.9*EMU), 'unit': 'EMU'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': int(0.55*EMU), 'translateY': int(0.5*EMU), 'unit': 'EMU'}
        }
    }})
    create_requests.append({'insertText': {'objectId': 's1_title', 'text': 'OpenClaw 소개', 'insertionIndex': 0}})
    create_requests.append({'createShape': {
        'objectId': 's1_sub',
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': 'slide1',
            'size': {'width': {'magnitude': int(9.3*EMU), 'unit': 'EMU'}, 'height': {'magnitude': int(0.6*EMU), 'unit': 'EMU'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': int(0.55*EMU), 'translateY': int(1.6*EMU), 'unit': 'EMU'}
        }
    }})
    create_requests.append({'insertText': {'objectId': 's1_sub', 'text': '간단 요약 (5장)', 'insertionIndex': 0}})

    slides = [
        ('slide2', 's2_title', 's2_body', 'OpenClaw는?', [
            '오픈소스 자동화/에이전트 프레임워크',
            '도구 연결과 워크플로우 실행에 초점',
            '커뮤니티 기반 확장성'
        ]),
        ('slide3', 's3_title', 's3_body', '핵심 기능', [
            '멀티툴 오케스트레이션',
            '에이전트 스킬/플러그인 구조',
            '작업 기록 및 자동화'
        ]),
        ('slide4', 's4_title', 's4_body', '활용 사례', [
            '리서치·요약 자동화',
            '슬라이드/문서 생성',
            '일상 업무 보조(캘린더, 메시징 등)'
        ]),
        ('slide5', 's5_title', 's5_body', '왜 OpenClaw인가', [
            '가볍고 유연한 구성',
            '투명한 오픈소스',
            '커뮤니티가 빠르게 개선'
        ]),
    ]

    for sid, title_id, body_id, title_text, bullets in slides:
        create_requests.append({'createSlide': {'objectId': sid, 'slideLayoutReference': {'predefinedLayout': 'BLANK'}}})
        create_requests.append({'createShape': {
            'objectId': title_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': sid,
                'size': {'width': {'magnitude': int(9.3*EMU), 'unit': 'EMU'}, 'height': {'magnitude': int(0.9*EMU), 'unit': 'EMU'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': int(0.55*EMU), 'translateY': int(0.5*EMU), 'unit': 'EMU'}
            }
        }})
        create_requests.append({'insertText': {'objectId': title_id, 'text': title_text, 'insertionIndex': 0}})
        create_requests.append({'createShape': {
            'objectId': body_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': sid,
                'size': {'width': {'magnitude': int(9.3*EMU), 'unit': 'EMU'}, 'height': {'magnitude': int(3.6*EMU), 'unit': 'EMU'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': int(0.55*EMU), 'translateY': int(1.5*EMU), 'unit': 'EMU'}
            }
        }})
        create_requests.append({'insertText': {'objectId': body_id, 'text': '\n'.join(bullets), 'insertionIndex': 0}})

    # Create slides
    batch_create = requests.post(
        f'https://gateway.maton.ai/google-slides/v1/presentations/{prez_id}:batchUpdate',
        headers=headers,
        json={'requests': create_requests}
    )
    batch_create.raise_for_status()

    # Apply styling
    batch_style = requests.post(
        f'https://gateway.maton.ai/google-slides/v1/presentations/{prez_id}:batchUpdate',
        headers=headers,
        json={'requests': build_requests()}
    )
    batch_style.raise_for_status()
    print(prez_id)


if __name__ == '__main__':
    main()
