# MONGODB QUICK REFERENCE CARD - DEMS EXAM
## Copy-Paste Ready Queries for MongoDB Compass

---

## DATABASE SELECTION IN COMPASS

**Switch between databases:**
- ems_db1 (Employees 1-1000)
- ems_db2 (Employees 1001-2000)
- ems_db3 (Employees 2001-3000)

---

## 1. BASIC QUERIES (Copy & Paste in Filter Box)

### Find All
```json
{}
```

### Find by Department
```json
{ "department": "Information Technology" }
```

### Find by Salary Range
```json
{ "salary": { "$gte": 50000, "$lte": 80000 } }
```

### Find Active Employees
```json
{ "status": "Active" }
```

### Find Pending Leaves
```json
{ "status": "Pending" }
```

### Find by Employee ID
```json
{ "emp_id": 101 }
```

### Find by Multiple Departments
```json
{ "department": { "$in": ["Information Technology", "Finance", "Marketing"] } }
```

### Find High Earners
```json
{ "salary": { "$gt": 70000 } }
```

---

## 2. AGGREGATION QUERIES (Use Aggregation Tab)

### Count Employees by Department
```json
[
  {
    "$group": {
      "_id": "$department",
      "count": { "$sum": 1 }
    }
  },
  {
    "$sort": { "count": -1 }
  }
]
```

### Average Salary by Department
```json
[
  {
    "$group": {
      "_id": "$department",
      "avgSalary": { "$avg": "$salary" },
      "minSalary": { "$min": "$salary" },
      "maxSalary": { "$max": "$salary" },
      "employeeCount": { "$sum": 1 }
    }
  },
  {
    "$sort": { "avgSalary": -1 }
  }
]
```

### Total Salary by Department
```json
[
  {
    "$group": {
      "_id": "$department",
      "totalSalary": { "$sum": "$salary" },
      "avgSalary": { "$avg": "$salary" },
      "count": { "$sum": 1 }
    }
  },
  {
    "$sort": { "totalSalary": -1 }
  }
]
```

### Top 5 Highest Paid
```json
[
  {
    "$sort": { "salary": -1 }
  },
  {
    "$limit": 5
  },
  {
    "$project": {
      "_id": 0,
      "name": 1,
      "department": 1,
      "position": 1,
      "salary": 1
    }
  }
]
```

### Count Leaves by Status
```json
[
  {
    "$group": {
      "_id": "$status",
      "count": { "$sum": 1 }
    }
  }
]
```

### Salary Statistics
```json
[
  {
    "$group": {
      "_id": null,
      "totalBaseSalary": { "$sum": "$base_salary" },
      "totalAllowances": { "$sum": "$allowances" },
      "totalDeductions": { "$sum": "$deductions" },
      "totalNetSalary": { "$sum": "$net_salary" },
      "avgNetSalary": { "$avg": "$net_salary" }
    }
  }
]
```

### Employees by Position Count
```json
[
  {
    "$group": {
      "_id": "$position",
      "count": { "$sum": 1 },
      "avgSalary": { "$avg": "$salary" }
    }
  },
  {
    "$sort": { "count": -1 }
  }
]
```

---

## 3. COMPLEX AGGREGATIONS

### Departments with More Than 1 Employee
```json
[
  {
    "$group": {
      "_id": "$department",
      "count": { "$sum": 1 }
    }
  },
  {
    "$match": { "count": { "$gt": 1 } }
  },
  {
    "$sort": { "count": -1 }
  }
]
```

### IT Department Statistics
```json
[
  {
    "$match": { "department": "Information Technology" }
  },
  {
    "$group": {
      "_id": null,
      "totalEmployees": { "$sum": 1 },
      "avgSalary": { "$avg": "$salary" },
      "totalSalaryExpense": { "$sum": "$salary" },
      "minSalary": { "$min": "$salary" },
      "maxSalary": { "$max": "$salary" }
    }
  }
]
```

### Leave Statistics by Employee
```json
[
  {
    "$group": {
      "_id": "$emp_id",
      "totalLeaves": { "$sum": 1 },
      "approved": {
        "$sum": { "$cond": [{ "$eq": ["$status", "Approved"] }, 1, 0] }
      },
      "pending": {
        "$sum": { "$cond": [{ "$eq": ["$status", "Pending"] }, 1, 0] }
      },
      "rejected": {
        "$sum": { "$cond": [{ "$eq": ["$status", "Rejected"] }, 1, 0] }
      }
    }
  },
  {
    "$sort": { "totalLeaves": -1 }
  }
]
```

### Monthly Salary Trends
```json
[
  {
    "$group": {
      "_id": {
        "year": "$year",
        "month": "$month"
      },
      "totalPaid": { "$sum": "$net_salary" },
      "avgSalary": { "$avg": "$net_salary" },
      "employeeCount": { "$sum": 1 }
    }
  },
  {
    "$sort": { "_id.year": -1, "_id.month": -1 }
  }
]
```

---

## 4. JOIN QUERIES (Aggregation Tab)

### Employees with Leave Count
```json
[
  {
    "$lookup": {
      "from": "leaves",
      "localField": "emp_id",
      "foreignField": "emp_id",
      "as": "leave_records"
    }
  },
  {
    "$project": {
      "name": 1,
      "department": 1,
      "totalLeaves": { "$size": "$leave_records" }
    }
  },
  {
    "$sort": { "totalLeaves": -1 }
  }
]
```

### Employees with Approved Leaves Only
```json
[
  {
    "$lookup": {
      "from": "leaves",
      "let": { "emp_id": "$emp_id" },
      "pipeline": [
        {
          "$match": {
            "$expr": { "$eq": ["$emp_id", "$$emp_id"] },
            "status": "Approved"
          }
        }
      ],
      "as": "approved_leaves"
    }
  },
  {
    "$project": {
      "name": 1,
      "department": 1,
      "approvedCount": { "$size": "$approved_leaves" }
    }
  }
]
```

### Employees with Salary History Count
```json
[
  {
    "$lookup": {
      "from": "salaries",
      "localField": "emp_id",
      "foreignField": "emp_id",
      "as": "salary_records"
    }
  },
  {
    "$project": {
      "name": 1,
      "department": 1,
      "current_salary": "$salary",
      "recordCount": { "$size": "$salary_records" }
    }
  }
]
```

---

## 5. DATE QUERIES

### Employees Joined in 2024
```json
{
  "join_date": {
    "$gte": { "$date": "2024-01-01T00:00:00Z" },
    "$lt": { "$date": "2025-01-01T00:00:00Z" }
  }
}
```

### Leaves Applied This Year
```json
{
  "applied_date": {
    "$gte": { "$date": "2024-01-01T00:00:00Z" }
  }
}
```

### Salaries Paid in 2024
```json
{
  "year": 2024
}
```

---

## 6. STRING/REGEX QUERIES

### Names Starting with 'S'
```json
{ "name": { "$regex": "^S", "$options": "i" } }
```

### Positions Containing 'Engineer'
```json
{ "position": { "$regex": "Engineer", "$options": "i" } }
```

### Emails from Specific Domain
```json
{ "email": { "$regex": "@company\\.com$" } }
```

---

## 7. DISTRIBUTED DATABASE QUERIES

### Query Each Database Fragment

**In ems_db1:**
```json
{ "emp_id": { "$lte": 1000 } }
```

**In ems_db2:**
```json
{ "emp_id": { "$gte": 1001, "$lte": 2000 } }
```

**In ems_db3:**
```json
{ "emp_id": { "$gte": 2001, "$lte": 3000 } }
```

### Count in Each Database
```json
[
  {
    "$group": {
      "_id": null,
      "total": { "$sum": 1 }
    }
  }
]
```

---

## 8. UPDATE QUERIES (mongosh commands)

### Update Single Field
```javascript
db.employees.updateOne(
  { "emp_id": 101 },
  { "$set": { "salary": 75000 } }
)
```

### Update Multiple Fields
```javascript
db.employees.updateOne(
  { "emp_id": 101 },
  { 
    "$set": { 
      "salary": 80000,
      "position": "Senior Software Engineer"
    } 
  }
)
```

### Update Multiple Documents
```javascript
db.employees.updateMany(
  { "department": "Information Technology" },
  { "$mul": { "salary": 1.10 } }
)
```

### Approve Leave
```javascript
db.leaves.updateOne(
  { "_id": ObjectId("your_id_here") },
  { 
    "$set": { 
      "status": "Approved",
      "approved_by": "admin",
      "approved_date": new Date()
    } 
  }
)
```

---

## 9. INSERT QUERIES (mongosh commands)

### Insert Employee
```javascript
db.employees.insertOne({
  "emp_id": 108,
  "name": "Test Employee",
  "email": "test@company.com",
  "phone": "01712345678",
  "department": "Information Technology",
  "position": "Developer",
  "salary": 55000,
  "date_of_birth": "1995-01-01",
  "join_date": new Date(),
  "status": "Active",
  "created_at": new Date()
})
```

### Insert Leave
```javascript
db.leaves.insertOne({
  "emp_id": 108,
  "start_date": "2024-12-20",
  "end_date": "2024-12-22",
  "leave_type": "Casual",
  "reason": "Personal work",
  "status": "Pending",
  "applied_date": new Date(),
  "approved_by": null,
  "approved_date": null
})
```

---

## 10. DELETE QUERIES (mongosh commands)

### Delete Single Employee
```javascript
db.employees.deleteOne({ "emp_id": 108 })
```

### Delete Rejected Leaves
```javascript
db.leaves.deleteMany({ "status": "Rejected" })
```

### Delete Old Records
```javascript
db.salaries.deleteMany({ 
  "year": { "$lt": 2023 } 
})
```

---

## EXAM SHORTCUTS

### Quick Counts
```javascript
db.employees.countDocuments()
db.employees.countDocuments({ "status": "Active" })
db.leaves.countDocuments({ "status": "Pending" })
```

### Quick Sorts
```javascript
// Top salaries
db.employees.find().sort({ "salary": -1 }).limit(5)

// Newest employees
db.employees.find().sort({ "join_date": -1 }).limit(10)

// Alphabetical
db.employees.find().sort({ "name": 1 })
```

### Quick Projections
```javascript
// Name and salary only
db.employees.find({}, { "name": 1, "salary": 1, "_id": 0 })

// All except password
db.users.find({}, { "password": 0 })
```

---

## COMMON EXAM QUESTIONS - INSTANT ANSWERS

**Q: Count employees in each department**
```json
[{"$group":{"_id":"$department","count":{"$sum":1}}},{"$sort":{"count":-1}}]
```

**Q: Average salary by department**
```json
[{"$group":{"_id":"$department","avgSalary":{"$avg":"$salary"}}},{"$sort":{"avgSalary":-1}}]
```

**Q: Top 5 highest paid**
```json
[{"$sort":{"salary":-1}},{"$limit":5}]
```

**Q: Employees with salary > 60000**
```json
{"salary":{"$gt":60000}}
```

**Q: IT employees only**
```json
{"department":"Information Technology"}
```

**Q: Active employees in IT**
```json
{"department":"Information Technology","status":"Active"}
```

**Q: Pending leaves**
```json
{"status":"Pending"}
```

**Q: Total salary expense**
```json
[{"$group":{"_id":null,"total":{"$sum":"$salary"}}}]
```

---

## MONGODB COMPASS TIPS

1. **Filter Tab**: Paste JSON queries directly
2. **Aggregation Tab**: Build pipeline step-by-step
3. **Schema Tab**: See data structure
4. **Explain Plan**: Check query performance
5. **Export**: Download results as JSON/CSV

---

## OPERATOR QUICK REFERENCE

```
$eq   = equal
$ne   ≠ not equal
$gt   > greater than
$gte  ≥ greater or equal
$lt   < less than
$lte  ≤ less or equal
$in   ∈ in array
$nin  ∉ not in array

$and  logical AND
$or   logical OR
$not  logical NOT

$sum    Σ sum
$avg    x̄ average
$min    minimum
$max    maximum
$count  count
```

---

**GOOD LUCK! 🍀**

Practice these in MongoDB Compass before your exam!
