# PHASE 1: REGISTRATION & LOGIN

![Phase 1 Screenshot](grant_system/assets/Screenshot%202025-11-23%20233138.png)

### Key Implementation:
- **Django Form:** `UserCreationForm` extended with `role` field  
- **View Logic:** User registers → check `user.role` → redirect to Correct Dashboard  
- **Template:** Dropdown with 3 role options (Applicant / Reviewer / Admin)

# PHASE 2: APPLICANT WORKFLOW

## Applicant Workflow
![Applicant Workflow Screenshot](grant_system/assets/image.png)
## Django Components Used

### ✔ View  
`applicant_dashboard()`

- Queries: `Application.objects.filter(applicant=request.user)`

### ✔ Template  
`applicant/dashboard.html`

- Renders applications table  
- Uses `{% for app in applications %}` loop

### ✔ Form (ModelForm)  
`ApplicationForm`

- Handles file upload  
- Includes built-in validation

### ✔ View  
`submit_application()`

- Saves form using `form.save(commit=False)`  
- Sets `application.applicant = request.user`  
- Calls `application.save()`



# PHASE 3: ADMIN WORKFLOW

![Admin Screenshot 1](grant_system/assets/Screenshot%202025-11-24%20030109.png)
![Admin Screenshot 2](grant_system/assets/Screenshot%202025-11-24%20030131.png)

## Django Components

### ✔ View  
`assign_reviewers()`

- Gets all users where `role='reviewer'`

### ✔ Template  
- Displays checkbox list of reviewers

### ✔ Logic  
- Creates multiple `Review` objects in a loop  
- Assigns selected reviewers

### ✔ Status Update  
- Updates `Application.status`  
  - From `"submitted"` → `"in_review"`



# PHASE 4: REVIEWER WORKFLOW (BLINDED REVIEW)

![Reviewer Screenshot](grant_system/assets/Screenshot%202025-11-24%20030608.png)
