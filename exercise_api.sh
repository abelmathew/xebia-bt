#!/bin/bash

echo "--- Normal ---"
curl -v -H "Content-Type: application/json" -d "{ \"username\": \"amathew\", \"password\": \"salted\"}" "http://localhost:5000/login" 
echo

echo "--- Normal + App Version ---"
curl -v -H "Content-Type: application/json" -d "{ \"username\": \"amathew\", \"password\": \"salted\", \"app_version\": \"0.1.2\"}" "http://localhost:5000/login" 
echo

