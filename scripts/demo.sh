#!/bin/bash

# Проверка наличия jq
if ! command -v jq &> /dev/null; then
    echo "Утилита jq не найдена. Установите её с помощью 'sudo apt install jq'"
    exit 1
fi

BASE_URL="http://localhost:8000"

echo "=== Демонстрация работы API ==="

echo "1. Регистрация нового пользователя..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/registration/" \
    -H "Content-Type: application/json" \
    -d "{
        \"username\": \"testuser\",
        \"email\": \"test@somesite.ru\",
        \"password\": \"very-bad-password\"
    }")
echo -e "Ответ на регистрацию: $REGISTER_RESPONSE\n"

echo "2. Авторизация пользователя..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/token/" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "testuser",
        "password": "very-bad-password"
    }')
echo -e "Ответ на авторизацию: $LOGIN_RESPONSE\n"

ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access')
if [ -z "$ACCESS_TOKEN" ]; then
    echo "Ошибка авторизации. Проверьте данные."
    exit 1
fi
echo -e "Токен доступа: $ACCESS_TOKEN\n"

REFRESH_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.refresh')
if [ -z "$REFRESH_TOKEN" ]; then
    echo "Ошибка авторизации. Проверьте данные."
    exit 1
fi
echo -e "Рефреш токен: $REFRESH_TOKEN\n"

echo "3. Получение профиля пользователя..."
PROFILE_RESPONSE=$(curl -s -X GET "$BASE_URL/api/profile/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
echo -e "Ответ на запрос профиля: $PROFILE_RESPONSE\n"

echo "4. Запрос награды..."
REWARD_REQUEST_RESPONSE=$(curl -s -X POST "$BASE_URL/api/rewards/request/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
echo -e "Ответ на запрос награды: $REWARD_REQUEST_RESPONSE\n"

echo "5. Просмотр списка наград..."
REWARDS_RESPONSE=$(curl -s -X GET "$BASE_URL/api/rewards/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
echo -e "Ответ на запрос списка наград: $REWARDS_RESPONSE\n"

echo "6. Обновление токена..."
TOKEN_REFRESH_RESPONSE=$(curl -s -X POST "$BASE_URL/api/token/refresh/" \
    -H "Content-Type: application/json" \
    -d "{\"refresh\": \"$REFRESH_TOKEN\"}")
echo -e "Ответ на обновление токена: $TOKEN_REFRESH_RESPONSE\n"

NEW_ACCESS_TOKEN=$(echo "$TOKEN_REFRESH_RESPONSE" | jq -r '.access')
if [ -z "$NEW_ACCESS_TOKEN" ]; then
    echo "Ошибка обновления токена. Проверьте данные."
    exit 1
fi
echo -e "Новый токен доступа: $NEW_ACCESS_TOKEN\n"

# Сравнение старого и нового токенов
if [ "$ACCESS_TOKEN" == "$NEW_ACCESS_TOKEN" ]; then
    echo "Ошибка: Новый токен совпадает со старым. Обновление токена не работает."
    exit 1
else
    echo -e "Новый токен отличается от старого. Обновление токена работает корректно.\n"
fi

echo "7. Проверка нового токена (получение профиля)..."
PROFILE_RESPONSE_WITH_NEW_TOKEN=$(curl -s -X GET "$BASE_URL/api/profile/" \
    -H "Authorization: Bearer $NEW_ACCESS_TOKEN")
echo -e "Ответ на запрос профиля с новым токеном: $PROFILE_RESPONSE_WITH_NEW_TOKEN\n"

echo "=== Демонстрация завершена ==="