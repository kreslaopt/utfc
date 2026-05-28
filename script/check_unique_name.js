const fs = require('fs');
const path = require('path');

const directoryPath = 'C:\\Users\\UTFC\\Documents\\БалтМебель\\to\\products';

function readJsonFile(filePath) {
    try {
        const data = fs.readFileSync(filePath, 'utf8');
        return JSON.parse(data);
    } catch (err) {
        console.error('Ошибка чтения или парсинга файла:', filePath, err);
        return null;
    }
}

function scanDirectory(dir) {
    const files = fs.readdirSync(dir);
    files.forEach(file => {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
            // Рекурсивный вызов для подпапки
            scanDirectory(fullPath);
        } else if (path.extname(fullPath).toLowerCase() === '.json') {
            const jsonData = readJsonFile(fullPath);
            if (jsonData && !jsonData.unique_name) {
                console.log('Отсутствует unique_name в файле:', fullPath);
            }
        }
    });
}

scanDirectory(directoryPath);