const fs = require('fs');
const path = require('path');

const productsDir = path.join(__dirname, '../products');
const gasliftsSet = new Set();

// Рекурсивная функция поиска свойства "Газлифт" внутри JSON
function findGasliftInObject(obj) {
    if (typeof obj !== 'object' || obj === null) return;

    for (const key in obj) {
        if (!obj.hasOwnProperty(key)) continue;
        const value = obj[key];

        // Проверяем, если ключ содержит "газлифт" (игнорируем регистр)
        if (key.toLowerCase().includes('газлифт')) {
            if (typeof value === 'string') {
                gasliftsSet.add(value);
            }
        }

        // Рекурсивный вызов для вложенных объектов
        if (typeof value === 'object') {
            findGasliftInObject(value);
        }
    }
}

// Обход папок и обработка JSON-файлов
function collectGaslifts(dir) {
    const files = fs.readdirSync(dir);
    files.forEach(file => {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
            collectGaslifts(fullPath);
        } else if (file.endsWith('.json')) {
            try {
                const data = fs.readFileSync(fullPath, 'utf-8');
                const json = JSON.parse(data);
                // Вызов рекурсивной функции поиска "Газлифт" внутри JSON
                findGasliftInObject(json);
            } catch (err) {
                console.error(`Ошибка при чтении файла ${fullPath}:`, err);
            }
        }
    });
}

// Запускаем сбор
collectGaslifts(productsDir);

// Выводим все уникальные значения газлифта
console.log('Газлифты:', Array.from(gasliftsSet));