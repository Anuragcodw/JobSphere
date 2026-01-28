## Live Demo

https://jobsphere-eb2e.onrender.com

This project is fully deployed on Render and accessible publicly 

# Local Job Portal

A full-stack job portal built with Flask where users can search jobs, apply, manage profiles,
and admins can control jobs, users, reviews, and analytics.

## Overview

Local Job Portal is a production-style web application that connects job seekers with employers.
Users can search real jobs, apply, upload resumes, and manage profiles.
Admins can manage users, approve jobs, monitor reviews, and view analytics.

## Features

### User Side
- User registration & login
- Search jobs using external API
- View job details with map location
- Apply for jobs
- Profile management
- Resume upload & parsing
- Job reviews & ratings

### Admin Side
- Admin dashboard
- User management (block/activate)
- Job approval system
- Job management
- Reviews monitoring
- Analytics dashboard (users, jobs, ratings)

## Tech Stack

- Backend: Python (Flask)
- Database: MySQL + SQLAlchemy ORM
- Frontend: HTML, CSS, Bootstrap
- JavaScript for UI & maps
- External Job API integration


## Project Structure

local_job_portal/
│
├── app/
│   ├── models/
│   ├── routes/
│   ├── templates/
│   └── services/
│
├── admin/
├── static/
├── run.py
├── requirements.txt
└── README.md

## Default Admin

Email: admin@example.com  
Password: admin123

## Future Scope

- Company dashboard
- Email notifications
- Advanced analytics charts
- Mobile responsive PWA
- AI-based job recommendations

