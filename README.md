# AI Resume Screening Agent

An AI-powered resume screening agent that parses resumes, extracts candidate information, compares candidates against a job description, calculates relevance scores, and ranks candidates based on their suitability for the role.

## Overview

This project was developed as part of the Rooman Technologies Junior AI Research Associate AI Challenge.

The agent screens multiple resumes against a given job description and produces an ordered ranking with:

- Candidate information
- Required skill matches
- Missing required skills
- Semantic relevance score
- Skill match score
- Experience score
- Final score
- Recommendation
- Reasoning for the ranking

The system supports TXT, PDF, and DOCX resumes.

## Features

- Parse TXT resumes
- Parse PDF resumes
- Parse DOCX resumes
- Extract candidate name
- Extract education
- Extract experience
- Extract skills
- Extract required skills from a job description
- Calculate semantic similarity using Sentence Transformers
- Calculate required skill coverage
- Calculate experience fit
- Generate a weighted final score
- Rank candidates automatically
- Identify matched skills
- Identify missing skills
- Generate candidate recommendations
- Generate ranking explanations
- Export ranked results to CSV
- Export ranked results to JSON
- Automated tests using pytest

## Architecture

```text
Resume Files
    |
    v
+----------------+
| Resume Parser  |
+----------------+
    |
    v
+----------------------+
| Information Extractor|
+----------------------+
    |
    +--------------------+
    |                    |
    v                    v
Candidate Data       Job Description
    |                    |
    +---------+----------+
              |
              v
       +-------------+
       | AI Scoring  |
       +-------------+
              |
       +------+------+
       |      |      |
       v      v      v
   Semantic  Skill  Experience
   Score     Score  Score
       \      |      /
        \     |     /
         v    v    v
       Final Score
              |
              v
        Candidate Ranking
              |
       +------+------+
       |             |
       v             v
      CSV           JSON