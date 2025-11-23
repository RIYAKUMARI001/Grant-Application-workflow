# PHASE 1: REGISTRATION & LOGIN

![Phase 1 Screenshot](assets/Screenshot 2025-11-23 233138.png)



# PHASE 2: APPLICANT WORKFLOW

![Applicant Workflow](assets/image.png)

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
- Built-in validation

### ✔ View  
`submit_application()`  
- Saves form using `form.save(commit=False)`  
- Sets `application.applicant = request.user`  
- Finally: `application.save()`



# PHASE 3: ADMIN WORKFLOW

![Admin Screenshot 1](assets/Screenshot 2025-11-24 030109.png)
![Admin Screenshot 2](assets/Screenshot 2025-11-24 030131.png)

## Django Components

### ✔ View  
`assign_reviewers()`  
- Gets all users where `role='reviewer'`

### ✔ Template  
- Checkbox list to select multiple reviewers

### ✔ Logic  
- Creates multiple `Review` objects in a loop  
- Assigns selected reviewers

### ✔ Status Update  
- Changes `Application.status`  
  - From `"submitted"` → `"in_review"`



# PHASE 4: REVIEWER WORKFLOW (BLINDED REVIEW)

![Reviewer Screenshot](assets/Screenshot 2025-11-24 030608.png)

