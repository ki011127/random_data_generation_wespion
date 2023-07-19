const spawn = require('child_process').spawn;
const xlsx = require( "xlsx" );

// 2. spawn을 통해 "python 파이썬파일.py" 명령어 실행
const min = 100;
const range = 40;
const rep = 6;
const duration = 1.5
const result = spawn('python', ['random_generator.py',min,range,rep,duration]);


//3. stdout의 'data'이벤트리스너로 실행결과를 받는다.
result.stdout.on('data', function(data) {
});

// 4. 에러 발생 시, stderr의 'data'이벤트리스너로 실행결과를 받는다.
result.stderr.on('data', function(data) {
    console.log(data.toString());
});

result.on('close', function(code){
    const excelFile = xlsx.readFile( "random_generator.xlsx");
    const sheetName = excelFile.SheetNames[0];
    const firstSheet = excelFile.Sheets[sheetName];
    const jsonData = xlsx.utils.sheet_to_json( firstSheet, { defval : "", header: 2, } );
    console.log(jsonData);
    
});
     