# Frontend technical test

The goal of the project is to create a Quiz web app. A quiz represent a set of questions with one valid answer for each. We won't be evaluating the aesthetic appearance, only the structure and code quality of the result. The constraints are the following:

- You need to use the last version of Angular and Angular Material
- We will provide you with the backend, you will need to run it and be able to read its documentation to call its APIs
- You must send to us the completed project with a comprehensible set of instructions to run it in a README

The app must do the following:

- On the homepage, display all registered quizzes.
- On the homepage, add a button to create a new quiz. This take you to a creation form and if you complete it, the new quiz is registered and appears in the homepage. This form can be completed from a single or multiple pages, the choice is yours.
- If you click on one of the quizzes displayed in the homepage, you will then be able to take the selected quiz and get a result back at the end after validating your answers.
- Bonus (Level \*):  
    Use the LocalStorage to keep in memory the quizzes that are already answered and their score; display the score and block the possibility to retake any already taken quiz from the homepage (this system is of course unreliable and not secure; never use this in production!)
- Bonus (Level \*\*\*):  
    Add the possibility to edit an existing quiz (quiz question order does not matter)
- Bonus (Level \*\*\*\*\*):
  > /!\ This will necessitate editing the backend

  Add the possibility to reorder the questions of a quiz

**Keep it as simple as you can. You are free to chose for anything that is not explicitly mentioned in the problem statement.**
