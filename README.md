# AI_SnakeGame
<img width="75%" src="https://user-images.githubusercontent.com/81283189/181182186-a916b4fd-76c1-4e29-a758-b75f67c247f7.png" />


## Rule
1. 뱀은 자신의 머리가 자신의 몸, 벽, 상대 뱀의 몸에 닿으면 죽는다.
2. 뱀이 죽으면 점수가 -1점 된다. (최종 점수가 음수일 수도 있다)
3. 죽으면 시작 위치에서 몸 길이 4칸으로 리스폰된다
4. 열매를 먹으면 뱀의 몸 길이가 1칸 늘어나고 점수가 +1점 된다.
5. 1분동안 게임이 진행되며 1분 후 점수가 더 높은 쪽이 승리한다.
6. 빨간 뱀이 인간, 햐안 뱀이 인공지능이다.

## Run
1. github 화면에서 'code'라고 적힌 초록색 버튼을 눌러 'download zip'을 누른다.
2. 다운로드 받은 zip파일 압축해제하고 exe 폴더의 Snake.exe를 눌러 게임을 실행한다.
3. <b>exe 폴더 내의 파일들은 Snake.exe와 같은 폴더 내에 있어야 게임이 실행된다.</b>

## Control
1. 방향키로 뱀의 진행 방향을 조절한다.
2. 게임 도중 space바를 누르면 게임이 멈춘다.
3. 게임이 멈춘 상태에서 C를 누르면  게임 재시작, ESC를 누르면 게임 종료된다.
4. 1분이 지나면 게임이 종료되고 게임 결과가 화면에 표시된다. 
5. 게임 종료시 오류창이 뜨는데 x를 눌러 닫아준다.

## Dependencies

* Python 3+
* numpy
* pygame
* pickle
* random
* pyinstaller

Snake game code by HonzaKral: https://gist.github.com/HonzaKral/833ee2b30231c53ec78e    
Genetic algorithm by kairess: https://github.com/kairess/genetic_snake
