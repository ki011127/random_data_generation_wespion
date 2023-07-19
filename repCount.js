const spawn = require('child_process').spawn;
const { exec } = require('child_process');
const xlsx = require( "xlsx" );

// 2. spawn을 통해 "python 파이썬파일.py" 명령어 실행
const min_location = 100;
const range = 40;
const num_of_rep = 6;
const duration = 1.5
const result = spawn('python', ['random_generator.py',min_location,range,num_of_rep,duration]);


//3. stdout의 'data'이벤트리스너로 실행결과를 받는다.
result.stdout.on('data', function(data) {
});

// 4. 에러 발생 시, stderr의 'data'이벤트리스너로 실행결과를 받는다.
result.stderr.on('data', function(data) {
    console.log(data.toString());
});

let i = 0;
let rep = 0; // 실제 rep count
let max = 0; // 각 rep의 최댓값
let min = 500; // 각 rep의 최솟값
let tempMax = 0; // 기준에 못 미치는 최대값을 저장
const exerMax = []; // 기준이 될 만한 최댓값 저장
const exerMin = []; // 기준이 될 만한 최솟값 저장
let isUp = 1; // 현재 위치가 커지는 중인지 아닌지 판별
let count = 0; // 몇 번째 데이터인지 확인
let tempData = 0; // 50ms 이전의 데이터 저장
let minAvg;
let maxAvg;
let time = 0;
let diffAverage = 0;
let for_graph_location = []
let for_graph_time = []
function counting(data){
    if(count%5===0){ // 50ms 마다 확인
        if(data.location-tempData>=1.0){ // 내리다가 올리는 상황이 되는 경우
            if(isUp===0 && exerMin.length === 0){
                for_graph_location.push(min);
                for_graph_time.push(time)
                exerMin.push(min);
                rep++;
            }
            else if(isUp===0){
                minAvg = exerMin.reduce((accumulator, currentValue) => {
                    return accumulator + currentValue;
                }, 0) / (exerMin.length);
                let sum = 0;
                let len = exerMin.length;
                for (let i = 0; i < len; i++) {
                    sum += exerMax[i] - exerMin[i];
                }
                diffAverage = sum / len;
                if(min-minAvg<10 || diffAverage<tempMax-min){ // 충분히 내린 경우(최저점이 기준에 근접한 경우)
                    exerMin.push(min);
                }
                else{
                    // 코칭 시스템 관련 코드 작성
                }
                if((diffAverage*0.5)-(tempMax-min)<=0){ // 가동 범위 평균의 절반 이상으로 운동한 경우 rep 증가
                    rep++;
                    for_graph_location.push(min);
                    for_graph_time.push(time);
                    console.log(rep);
                }
            }
            if(isUp===0){
                //save_packet(min, time);
                min = 500;
            }
            isUp = 1;
        }
        else if (tempData-data.location>=1.0){ // 올리다가 내리는 상황으로 바뀌는 경우
            if(exerMax.length === 0){
                exerMax.push(max);
            }
            else if(isUp===1){
                maxAvg = exerMax.reduce((accumulator, currentValue) => {
                    return accumulator + currentValue;
                }, 0) / (exerMax.length);
                if(maxAvg-max<5){
                    exerMax.push(max);
                }
                else{
                    // 코칭 시스템 관련 코드 추가
                }
                tempMax = max;
            }
            if(isUp===1){
                //save_packet(max, time);
                max = 0;
            }
            isUp = 0;
        }
        else{
            
        }
        tempData = data.location;
    }
    count++;
    if(data.location>max && isUp === 1){
        max = data.location;
        time = data.time;
    }
    else if(data.location<min && isUp === 0){
        //console.log("..");
        min = data.location;
        time = data.time;
    }

}

result.on('close', function(code){
    const excelFile = xlsx.readFile( "random_generator.xlsx");
    const sheetName = excelFile.SheetNames[0];
    const firstSheet = excelFile.Sheets[sheetName];
    const data = xlsx.utils.sheet_to_json( firstSheet, { defval : "", header: 2, } );
    //console.log(jsonData);
    let len = data.length;
    const intervalId = setInterval(() => {
        if (i < len) {
            counting(data[i]);
            i++;
        } else {
            clearInterval(intervalId);
            console.log(diffAverage);
            console.log(tempMax);
            console.log(minAvg);
            if(diffAverage*0.5<=tempMax-minAvg){
                rep++;
            }
            console.log(exerMax);
            console.log(exerMin);
            console.log("rep : " + rep);
            const graph = spawn('python', ['draw_graph.py', for_graph_location, for_graph_time]);
            graph.stdout.on('data', function(data) {
                console.log(data.toString());
            });
            
            // 4. 에러 발생 시, stderr의 'data'이벤트리스너로 실행결과를 받는다.
            graph.stderr.on('data', function(data) {
                console.log(data.toString());
            });
        }
    }, );
});
     