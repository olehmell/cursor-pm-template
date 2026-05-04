# PetID Prototype - Digital Vet Passport MVP

Інтерактивний прототип для валідації core hypothesis: "Користувачі хочуть зберігати медичні документи тварини в додатку через фото upload."

## 🎯 Що включено

Прототип містить 8 ключових екранів:

1. **Onboarding Upload** - крок 3/3 з можливістю завантажити фото паспорту
2. **Photo Preview** - перегляд фото перед завантаженням з інфо про compression
3. **Upload Progress** - прогрес бар завантаження
4. **Upload Success** - анімація успішного завантаження
5. **PetID Empty State** - порожній стан без документів
6. **PetID Gallery** - галерея завантажених документів (grid 2 колонки)
7. **Photo Viewer** - повноекранний перегляд документу з можливістю навігації
8. **Delete Confirmation** - модальне вікно підтвердження видалення

## 🚀 Як запустити

### Встановлення залежностей

```bash
yarn install
```

### Запуск dev сервера

```bash
yarn dev
```

Прототип буде доступний за адресою: `http://localhost:5173`

### Build для production

```bash
yarn build
```

### Preview production build

```bash
yarn preview
```

## 🛠 Технологічний стек

- **React 18** - UI фреймворк
- **TypeScript** - типізація
- **Tailwind CSS** - стилізація
- **Vite** - bundler та dev server
- **Lucide React** - іконки

## 📱 Дизайн

Прототип стилізований згідно з наданими скріншотами:

- Білий фон з мінімалістичним дизайном
- Зелений акцентний колір (`#10b981`)
- iPhone-style frame (375x812px)
- Bottom navigation (Home, Pets, Vets, Profile)
- Округлі кнопки та карточки

## 🎨 Структура проекту

```
src/
├── components/
│   ├── ui/
│   │   ├── Button.tsx          # Кнопки (primary, secondary, ghost)
│   │   ├── Modal.tsx           # Модальні вікна
│   │   └── ProgressBar.tsx     # Прогрес бар
│   └── layout/
│       ├── MobileFrame.tsx     # Рамка мобільного пристрою
│       ├── Header.tsx          # Хедер з навігацією
│       └── BottomNav.tsx       # Нижня навігація
├── screens/
│   ├── OnboardingUpload.tsx    # Екран onboarding
│   ├── PhotoPreview.tsx        # Превью фото
│   ├── UploadProgress.tsx      # Прогрес завантаження
│   ├── UploadSuccess.tsx       # Успішне завантаження
│   ├── PetIdEmpty.tsx          # Порожній стан
│   ├── PetIdGallery.tsx        # Галерея документів
│   └── PhotoViewer.tsx         # Повноекранний перегляд
├── App.tsx                     # Головний компонент з роутингом
├── main.tsx                    # Entry point
└── index.css                   # Tailwind imports + global styles
```

## 🔄 User Flow

```
Onboarding → Take Photo/Gallery → Photo Preview → Upload Progress 
→ Upload Success → PetID Gallery → Photo Viewer → Delete (optional)
```

## 📝 Примітки

- Використовуються placeholder images з Unsplash для демонстрації
- Upload симулюється з затримкою 3 секунди
- Всі дані зберігаються в стані компонента (без backend)
- Прототип оптимізований для мобільних пристроїв (375x812px)

## 🎯 Мета прототипу

Валідувати гіпотезу через user testing:
- Upload completion rate >40%
- Skip rate <60%
- User feedback: "корисна фіча" (>70% positive)

## 📄 Документація

Детальний PRD доступний в: `usecases/02-prd-writing/artifacts/epic-a-mvp-for-prototype.md`
