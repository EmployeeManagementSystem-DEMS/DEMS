# SAMPLE QUERIES WITH EXPECTED RESULTS
## Test These in MongoDB Compass to Verify Your Understanding

---

## SAMPLE DATA OVERVIEW

Based on your `init_data.py`, you have:

### Employees (7 total)
- **ems_db1** (IDs 1-1000): 101 (Sifat), 102 (Sara)
- **ems_db2** (IDs 1001-2000): 1001 (Bidhan), 1002 (Nafisa)
- **ems_db3** (IDs 2001-3000): 2001 (Rafiad), 2002 (Asif), 2003 (Chironjeet)

### Departments (5 total - replicated in all DBs)
- Human Resources
- Information Technology
- Finance
- Marketing
- Operations

---

## TEST QUERIES WITH EXPECTED RESULTS

### Test 1: Count All Employees in Each Database

**Query (run in each DB):**
```javascript
db.employees.countDocuments()
```

**Expected Results:**
- ems_db1: 2 employees
- ems_db2: 2 employees
- ems_db3: 3 employees
- **Total across all DBs: 7 employees**

---

### Test 2: Count Departments (Should be Same in All DBs)

**Query:**
```javascript
db.departments.countDocuments()
```

**Expected Result:**
- All 3 databases: 5 departments (replicated)

---

### Test 3: Find All IT Employees

**Query:**
```json
{ "department": "Information Technology" }
```

**Expected Results:**
- Should find employees from IT department
- Results depend on which database you're querying
- Check names match your data

---

### Test 4: Total Salary Expense by Department

**Query:**
```json
[
  {
    "$group": {
      "_id": "$department",
      "totalSalary": { "$sum": "$salary" },
      "count": { "$sum": 1 }
    }
  },
  {
    "$sort": { "totalSalary": -1 }
  }
]
```

**Expected Result Structure:**
```json
[
  {
    "_id": "Information Technology",
    "totalSalary": 190000,
    "count": 3
  },
  {
    "_id": "Finance",
    "totalSalary": 120000,
    "count": 2
  }
]
```
*(Values depend on your actual salary data)*

---

### Test 5: Employee Count by Department

**Query:**
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

**What to Check:**
- All departments should be listed
- Count should add up to total employees in that DB
- Results will vary by database (fragmentation)

---

### Test 6: Find Employees with Salary > 60000

**Query:**
```json
{ "salary": { "$gt": 60000 } }
```

**What to Check:**
- All returned employees have salary field > 60000
- No employee with salary ≤ 60000 appears

---

### Test 7: Average Salary by Department

**Query:**
```json
[
  {
    "$group": {
      "_id": "$department",
      "avgSalary": { "$avg": "$salary" },
      "minSalary": { "$min": "$salary" },
      "maxSalary": { "$max": "$salary" }
    }
  }
]
```

**What to Check:**
- avgSalary is between minSalary and maxSalary
- All values are numbers (not null)

---

### Test 8: Fragmentation Verification

**Test horizontal fragmentation:**

**In ems_db1:**
```json
{ "emp_id": { "$lte": 1000 } }
```
Expected: Only employees with IDs 1-1000 (e.g., 101, 102)

**In ems_db2:**
```json
{ "emp_id": { "$gte": 1001, "$lte": 2000 } }
```
Expected: Only employees with IDs 1001-2000 (e.g., 1001, 1002)

**In ems_db3:**
```json
{ "emp_id": { "$gte": 2001, "$lte": 3000 } }
```
Expected: Only employees with IDs 2001-3000 (e.g., 2001, 2002, 2003)

---

### Test 9: Replication Verification

**Query departments in all 3 databases:**
```javascript
db.departments.find().sort({ name: 1 })
```

**Expected:**
- All 3 databases return SAME departments
- Same dept_id, name, description
- This proves replication

---

### Test 10: Derived Fragmentation - Leaves

**In ems_db1:** Find leaves for employee 101
```json
{ "emp_id": 101 }
```

**In ems_db2:** Find leaves for employee 1001
```json
{ "emp_id": 1001 }
```

**In ems_db3:** Find leaves for employee 2001
```json
{ "emp_id": 2001 }
```

**Expected:**
- Leaves for employee 101 ONLY in ems_db1
- Leaves for employee 1001 ONLY in ems_db2
- Leaves for employee 2001 ONLY in ems_db3
- This proves derived fragmentation

---

### Test 11: Join - Employees with Leave Count

**Query:**
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
  }
]
```

**What to Check:**
- Each employee shows with their leave count
- Employees with no leaves show 0
- totalLeaves is a number

---

### Test 12: Complex - IT Employees with High Salary

**Query:**
```json
{
  "department": "Information Technology",
  "salary": { "$gt": 60000 }
}
```

**What to Check:**
- All results are from IT department
- All results have salary > 60000
- Both conditions are satisfied (AND logic)

---

### Test 13: OR Query - IT or Finance

**Query:**
```json
{
  "$or": [
    { "department": "Information Technology" },
    { "department": "Finance" }
  ]
}
```

**What to Check:**
- Results include employees from IT
- Results include employees from Finance
- No other departments appear

---

### Test 14: Leaves by Status

**Query:**
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

**Expected Result Example:**
```json
[
  { "_id": "Pending", "count": 3 },
  { "_id": "Approved", "count": 5 },
  { "_id": "Rejected", "count": 1 }
]
```

---

### Test 15: Top 3 Highest Paid

**Query:**
```json
[
  {
    "$sort": { "salary": -1 }
  },
  {
    "$limit": 3
  },
  {
    "$project": {
      "name": 1,
      "salary": 1,
      "_id": 0
    }
  }
]
```

**What to Check:**
- Exactly 3 results
- Results are in descending salary order
- First result has highest salary

---

## VALIDATION CHECKLIST

Before your exam, verify:

✅ **Database Connection**
- [ ] Can connect to all 3 databases in Compass
- [ ] Can switch between databases easily

✅ **Basic Queries**
- [ ] Can count documents in each collection
- [ ] Can find documents with filters
- [ ] Can sort results

✅ **Fragmentation**
- [ ] Employees correctly distributed by ID range
- [ ] Can query each fragment independently

✅ **Replication**
- [ ] Departments same in all databases
- [ ] Users same in all databases

✅ **Aggregation**
- [ ] Can group by fields
- [ ] Can calculate sum, avg, min, max
- [ ] Can sort aggregation results

✅ **Joins**
- [ ] Can join employees with leaves
- [ ] Can join employees with salaries
- [ ] Understand $lookup syntax

✅ **Complex Queries**
- [ ] Can combine AND/OR conditions
- [ ] Can filter and aggregate together
- [ ] Can use date range queries

---

## COMMON EXAM SCENARIOS

### Scenario 1: "Show me department-wise employee count"

**Query:**
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

---

### Scenario 2: "Find high-paid IT employees"

**Query:**
```json
{
  "department": "Information Technology",
  "salary": { "$gt": 70000 }
}
```

---

### Scenario 3: "Calculate average salary by position"

**Query:**
```json
[
  {
    "$group": {
      "_id": "$position",
      "avgSalary": { "$avg": "$salary" },
      "count": { "$sum": 1 }
    }
  },
  {
    "$sort": { "avgSalary": -1 }
  }
]
```

---

### Scenario 4: "Show pending leave requests"

**Query:**
```json
{ "status": "Pending" }
```

Or with employee details (join):
```json
[
  {
    "$match": { "status": "Pending" }
  },
  {
    "$lookup": {
      "from": "employees",
      "localField": "emp_id",
      "foreignField": "emp_id",
      "as": "employee_info"
    }
  }
]
```

---

### Scenario 5: "Find employees who joined in 2023"

**Query:**
```json
{
  "join_date": {
    "$gte": { "$date": "2023-01-01T00:00:00Z" },
    "$lt": { "$date": "2024-01-01T00:00:00Z" }
  }
}
```

---

### Scenario 6: "Total salary paid last month"

**Query in salaries collection:**
```json
[
  {
    "$match": {
      "year": 2024,
      "month": "November"
    }
  },
  {
    "$group": {
      "_id": null,
      "totalPaid": { "$sum": "$net_salary" }
    }
  }
]
```

---

### Scenario 7: "Employees with most approved leaves"

**Query:**
```json
[
  {
    "$match": { "status": "Approved" }
  },
  {
    "$group": {
      "_id": "$emp_id",
      "approvedCount": { "$sum": 1 }
    }
  },
  {
    "$sort": { "approvedCount": -1 }
  },
  {
    "$limit": 5
  }
]
```

---

### Scenario 8: "Departments with average salary > 60000"

**Query:**
```json
[
  {
    "$group": {
      "_id": "$department",
      "avgSalary": { "$avg": "$salary" }
    }
  },
  {
    "$match": {
      "avgSalary": { "$gt": 60000 }
    }
  },
  {
    "$sort": { "avgSalary": -1 }
  }
]
```

---

## DEBUGGING TIPS

### If query returns nothing:
1. Check collection name spelling
2. Check field name spelling (case-sensitive)
3. Verify you're in correct database
4. Check data actually exists

### If aggregation fails:
1. Test each stage separately
2. Remove $sort first, add back later
3. Check for syntax errors (missing commas, brackets)
4. Use Compass aggregation builder for visual help

### If counts don't match:
1. Remember fragmentation - each DB has subset
2. Check all 3 databases for total count
3. Use countDocuments() not deprecated count()

---

## FINAL CHECKLIST BEFORE EXAM

**Practice These:**
- [ ] 5 basic find queries
- [ ] 5 aggregation queries with $group
- [ ] 3 queries with $match and $group
- [ ] 2 join queries with $lookup
- [ ] 2 date range queries
- [ ] 2 OR/AND condition queries
- [ ] 1 complex nested aggregation

**Understand These Concepts:**
- [ ] Horizontal fragmentation (employee ID ranges)
- [ ] Data replication (departments, users)
- [ ] Derived fragmentation (leaves, salaries)
- [ ] Difference between find() and aggregate()
- [ ] When to use $match vs find()
- [ ] Purpose of $group, $sort, $project
- [ ] How $lookup joins collections

**Can Explain:**
- [ ] Why your project uses 3 databases
- [ ] How employees are distributed
- [ ] Why departments are replicated
- [ ] How leaves follow employee fragmentation

---

## CONFIDENCE BUILDER

**You know your project has:**
✅ 3 distributed databases
✅ 5 collections (employees, departments, users, leaves, salaries)
✅ Horizontal fragmentation for scalability
✅ Replication for availability
✅ Derived fragmentation for performance
✅ Real-world CRUD operations
✅ Complex aggregations for analytics

**You can demonstrate:**
✅ Basic queries (find, filter, sort)
✅ Aggregations (count, sum, average)
✅ Joins (employees with leaves/salaries)
✅ Distributed database concepts
✅ Data consistency across replicas
✅ Query optimization with indexes

---

**YOU'VE GOT THIS! 💪**

Practice in MongoDB Compass tonight.
Sleep well.
Trust your preparation.

**GOOD LUCK TOMORROW! 🎓🚀**
