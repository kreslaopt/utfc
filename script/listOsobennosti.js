const fs = require('fs');
const path = require('path');

const productsDir = path.join(__dirname, '../products');
const featuresMap = new Map();

function collectFeatures(dir) {
    const files = fs.readdirSync(dir);
    files.forEach(file => {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
            collectFeatures(fullPath);
        } else if (file.endsWith('.json')) {
            try {
                const data = fs.readFileSync(fullPath, 'utf-8');
                const json = JSON.parse(data);
                if (json.hasOwnProperty('Особенности')) {
                    const value = json['Особенности'];
                    if (typeof value === 'string') {
                        if (!featuresMap.has(value)) {
                            featuresMap.set(value, []);
                        }
                        featuresMap.get(value).push(fullPath);
                    }
                }
            } catch (err) {
                console.error(`Ошибка при чтении файла ${fullPath}:`, err);
            }
        }
    });
}

// Запуск
collectFeatures(productsDir);

// Вывод
console.log('Уникальные особенности и файлы:');
for (const [value, files] of featuresMap.entries()) {
    console.log(`Особенность: ${value}`);
    files.forEach(file => {
        console.log(`  файл: ${file}`);
    });
}



// const fs = require('fs');
// const path = require('path');

// const productsDir = path.join(__dirname, '../products');
// const featuresSet = new Set();

// // Обход папок и обработка JSON-файлов
// function collectFeatures(dir) {
//     const files = fs.readdirSync(dir);
//     files.forEach(file => {
//         const fullPath = path.join(dir, file);
//         const stat = fs.statSync(fullPath);
//         if (stat.isDirectory()) {
//             collectFeatures(fullPath);
//         } else if (file.endsWith('.json')) {
//             try {
//                 const data = fs.readFileSync(fullPath, 'utf-8');
//                 const json = JSON.parse(data);
//                 // Проверяем наличие свойства "Особенности"
//                 if (json.hasOwnProperty('Особенности')) {
//                     const value = json['Особенности'];
//                     if (typeof value === 'string') {
//                         featuresSet.add(value);
//                     }
//                 }
//             } catch (err) {
//                 console.error(`Ошибка при чтении файла ${fullPath}:`, err);
//             }
//         }
//     });
// }

// // Запускаем сбор
// collectFeatures(productsDir);

// // Выводим все уникальные значения "Особенности"
// console.log('Особенности:', Array.from(featuresSet)); 