const spawn = require('child_process').spawn

const pythonProcess = spawn('py', ['main.py', '36', '-80', '30', '2'])

pythonProcess.stdout.setEncoding('utf8')

async function pythonReturn () {
  pythonProcess.stdout.on('data', (data) => {
    console.log(data)
  })
}

pythonReturn()
