# MONGODB QUERIES GUIDE FOR DEMS
## Complete Query Reference for Distributed Database Lab Exam

**Project:** Distributed Employee Management System (DEMS)  
**Databases:** ems_db1, ems_db2, ems_db3 (MongoDB Atlas)  
**Tool:** MongoDB Compass  
**Date:** November 23, 2025

---

## TABLE OF CONTENTS

1. [Database Schema Overview](#database-schema-overview)
2. [Basic CRUD Operations](#basic-crud-operations)
3. [Conditional Queries (WHERE)](#conditional-queries-where)
4. [Comparison Operators](#comparison-operators)
5. [Logical Operators](#logical-operators)
6. [Aggregation Pipelines](#aggregation-pipelines)
7. [Sorting & Limiting](#sorting--limiting)
8. [Projection (Field Selection)](#projection-field-selection)
9. [Date & Time Queries](#date--time-queries)
10. [Array & String Operations](#array--string-operations)
11. [Join Operations ($lookup)](#join-operations-lookup)
12. [Distributed Database Queries](#distributed-database-queries)
13. [Index Operations](#index-operations)
14. [Practice Questions](#practice-questions)

---

## DATABASE SCHEMA OVERVIEW

### Collections Structure

**1. employees** (Fragmented across ems_db1, ems_db2, ems_db3)
```javascript
{
  emp_id: Number,           // Primary Key (1-3000)
  name: String,
  email: String,
  phone: String,
  department: String,
  position: String,
  salary: Number,
  date_of_birth: String,    // "YYYY-MM-DD"
  join_date: ISODate,
  status: String,           // "Active" or "Inactive"
  created_at: ISODate
}
```

**2. departments** (Replicated in all 3 databases)
```javascript
{
  dept_id: String,          // Primary Key
  name: String,
  description: String,
  manager: String,
  created_at: ISODate
}
```

**3. users** (Replicated in all 3 databases)
```javascript
{
  username: String,         // Primary Key
  password: String,         // bcrypt hashed
  role: String,             // "admin" or "employee"
  emp_id: Number,           // Foreign Key (nullable)
  created_at: ISODate
}
```

**4. leaves** (Derived fragmentation - same DB as employee)
```javascript
{
  _id: ObjectId,
  emp_id: Number,           // Foreign Key
  start_date: String,       // "YYYY-MM-DD"
  end_date: String,         // "YYYY-MM-DD"
  leave_type: String,       // "Sick", "Casual", "Annual"
  reason: String,
  status: String,           // "Pending", "Approved", "Rejected"
  applied_date: ISODate,
  approved_by: String,
  approved_date: ISODate
}
```

**5. salaries** (Derived fragmentation - same DB as employee)
```javascript
{
  emp_id: Number,           // Foreign Key
  pay_date: ISODate,
  month: String,
  year: Number,
  base_salary: Number,
  allowances: Number,
  deductions: Number,
  net_salary: Number,
  created_at: ISODate
}
```

### Database Distribution

- **ems_db1**: Employee IDs 1-1000
- **ems_db2**: Employee IDs 1001-2000
- **ems_db3**: Employee IDs 2001-3000

---

## BASIC CRUD OPERATIONS

### 1. INSERT (Create)

#### Insert Single Document
```javascript
// Insert employee in ems_db1 (ID 1-1000)
db.employees.insertOne({
  emp_id: 105,
  name: "John Doe",
  email: "john.doe@company.com",
  phone: "01712345678",
  department: "Information Technology",
  position: "Software Engineer",
  salary: 65000,
  date_of_birth: "1995-05-15",
  join_date: new Date("2023-01-10"),
  status: "Active",
  created_at: new Date()
})
```

#### Insert Multiple Documents
```javascript
// Insert multiple employees
db.employees.insertMany([
  {
    emp_id: 106,
    name: "Jane Smith",
    email: "jane.smith@company.com",
    phone: "01712345679",
    department: "Human Resources",
    position: "HR Manager",
    salary: 70000,
    date_of_birth: "1990-08-20",
    join_date: new Date("2022-03-15"),
    status: "Active",
    created_at: new Date()
  },
  {
    emp_id: 107,
    name: "Mike Johnson",
    email: "mike.johnson@company.com",
    phone: "01712345680",
    department: "Finance",
    position: "Accountant",
    salary: 55000,
    date_of_birth: "1993-12-10",
    join_date: new Date("2023-06-01"),
    status: "Active",
    created_at: new Date()
  }
])
```

#### Insert Department (Replicated)
```javascript
// Insert in all databases
db.departments.insertOne({
  dept_id: "DEPT006",
  name: "Research & Development",
  description: "Product research and innovation",
  manager: "Dr. Sarah Williams",
  created_at: new Date()
})
```

#### Insert Leave Request
```javascript
// Insert in same DB as employee
db.leaves.insertOne({
  emp_id: 105,
  start_date: "2024-12-20",
  end_date: "2024-12-25",
  leave_type: "Annual",
  reason: "Year-end vacation",
  status: "Pending",
  applied_date: new Date(),
  approved_by: null,
  approved_date: null
})
```

#### Insert Salary Record
```javascript
db.salaries.insertOne({
  emp_id: 105,
  pay_date: new Date("2024-11-30"),
  month: "November",
  year: 2024,
  base_salary: 65000,
  allowances: 5000,
  deductions: 3000,
  net_salary: 67000,
  created_at: new Date()
})
```

---

### 2. FIND (Read)

#### Find All Documents
```javascript
// Find all employees
db.employees.find()

// Find all with pretty formatting
db.employees.find().pretty()
```

#### Find One Document
```javascript
// Find employee by ID
db.employees.findOne({ emp_id: 105 })

// Find department by name
db.departments.findOne({ name: "Information Technology" })
```

#### Find with Specific Fields (Projection)
```javascript
// Show only name and salary
db.employees.find(
  {},
  { name: 1, salary: 1, _id: 0 }
)

// Show all except password
db.users.find(
  {},
  { password: 0 }
)
```

---

### 3. UPDATE

#### Update Single Document
```javascript
// Update employee salary
db.employees.updateOne(
  { emp_id: 105 },
  { $set: { salary: 70000 } }
)

// Update multiple fields
db.employees.updateOne(
  { emp_id: 105 },
  { 
    $set: { 
      salary: 75000,
      position: "Senior Software Engineer",
      department: "Research & Development"
    } 
  }
)
```

#### Update Multiple Documents
```javascript
// Give 10% raise to all IT employees
db.employees.updateMany(
  { department: "Information Technology" },
  { $mul: { salary: 1.10 } }
)

// Update all pending leaves to approved
db.leaves.updateMany(
  { status: "Pending" },
  { 
    $set: { 
      status: "Approved",
      approved_by: "admin",
      approved_date: new Date()
    } 
  }
)
```

#### Replace Document
```javascript
// Replace entire document (keep _id)
db.departments.replaceOne(
  { dept_id: "DEPT006" },
  {
    dept_id: "DEPT006",
    name: "R&D Department",
    description: "Research, Development and Innovation",
    manager: "Dr. Sarah Williams",
    created_at: new Date()
  }
)
```

---

### 4. DELETE

#### Delete Single Document
```javascript
// Delete employee
db.employees.deleteOne({ emp_id: 105 })

// Delete specific leave request
db.leaves.deleteOne({ 
  emp_id: 105,
  status: "Rejected"
})
```

#### Delete Multiple Documents
```javascript
// Delete all inactive employees
db.employees.deleteMany({ status: "Inactive" })

// Delete all rejected leaves
db.leaves.deleteMany({ status: "Rejected" })

// Delete old salary records (before 2023)
db.salaries.deleteMany({ 
  year: { $lt: 2023 } 
})
```

#### Delete All Documents (Keep Collection)
```javascript
// Delete all employees in this database
db.employees.deleteMany({})
```

---

## CONDITIONAL QUERIES (WHERE)

### Equality Conditions
```javascript
// Find employee by exact name
db.employees.find({ name: "Sifat Chowdhury" })

// Find all IT department employees
db.employees.find({ department: "Information Technology" })

// Find employees with specific position
db.employees.find({ position: "Software Engineer" })

// Find active employees
db.employees.find({ status: "Active" })
```

### Multiple Conditions (AND)
```javascript
// Find active IT employees
db.employees.find({
  department: "Information Technology",
  status: "Active"
})

// Find employees in IT with salary > 60000
db.employees.find({
  department: "Information Technology",
  salary: { $gt: 60000 }
})

// Find pending leaves for specific employee
db.leaves.find({
  emp_id: 101,
  status: "Pending"
})
```

---

## COMPARISON OPERATORS

### Greater Than ($gt)
```javascript
// Employees with salary > 60000
db.employees.find({ 
  salary: { $gt: 60000 } 
})

// Employees with emp_id > 1000 (in ems_db2 or ems_db3)
db.employees.find({ 
  emp_id: { $gt: 1000 } 
})
```

### Greater Than or Equal ($gte)
```javascript
// Employees with salary >= 50000
db.employees.find({ 
  salary: { $gte: 50000 } 
})

// Salary records for 2024 onwards
db.salaries.find({ 
  year: { $gte: 2024 } 
})
```

### Less Than ($lt)
```javascript
// Employees with salary < 50000
db.employees.find({ 
  salary: { $lt: 50000 } 
})

// Employees in first 1000 range (ems_db1)
db.employees.find({ 
  emp_id: { $lt: 1001 } 
})
```

### Less Than or Equal ($lte)
```javascript
// Employees with salary <= 60000
db.employees.find({ 
  salary: { $lte: 60000 } 
})
```

### Not Equal ($ne)
```javascript
// Find all non-IT employees
db.employees.find({ 
  department: { $ne: "Information Technology" } 
})

// Find all non-pending leaves
db.leaves.find({ 
  status: { $ne: "Pending" } 
})

// Find all non-admin users
db.users.find({ 
  role: { $ne: "admin" } 
})
```

### In Array ($in)
```javascript
// Employees from multiple departments
db.employees.find({ 
  department: { 
    $in: ["Information Technology", "Finance", "Marketing"] 
  } 
})

// Leaves with specific statuses
db.leaves.find({ 
  status: { $in: ["Approved", "Pending"] } 
})

// Employees with specific positions
db.employees.find({ 
  position: { 
    $in: ["Software Engineer", "Senior Software Engineer", "Team Lead"] 
  } 
})
```

### Not In Array ($nin)
```javascript
// Employees NOT from IT or HR
db.employees.find({ 
  department: { 
    $nin: ["Information Technology", "Human Resources"] 
  } 
})
```

### Range Queries
```javascript
// Employees with salary between 50000 and 80000
db.employees.find({ 
  salary: { $gte: 50000, $lte: 80000 } 
})

// Employees in ems_db2 range (1001-2000)
db.employees.find({ 
  emp_id: { $gte: 1001, $lte: 2000 } 
})
```

---

## LOGICAL OPERATORS

### AND ($and)
```javascript
// Explicit AND - Active IT employees with salary > 60000
db.employees.find({
  $and: [
    { department: "Information Technology" },
    { status: "Active" },
    { salary: { $gt: 60000 } }
  ]
})

// Implicit AND (same as above)
db.employees.find({
  department: "Information Technology",
  status: "Active",
  salary: { $gt: 60000 }
})
```

### OR ($or)
```javascript
// Employees from IT OR Finance
db.employees.find({
  $or: [
    { department: "Information Technology" },
    { department: "Finance" }
  ]
})

// High salary OR senior position
db.employees.find({
  $or: [
    { salary: { $gt: 80000 } },
    { position: { $regex: /Senior|Manager/, $options: "i" } }
  ]
})

// Leaves that are Approved OR Pending
db.leaves.find({
  $or: [
    { status: "Approved" },
    { status: "Pending" }
  ]
})
```

### NOT ($not)
```javascript
// Employees with salary NOT greater than 70000 (<=70000)
db.employees.find({ 
  salary: { $not: { $gt: 70000 } } 
})
```

### NOR ($nor)
```javascript
// Employees NOT in IT and NOT in Finance
db.employees.find({
  $nor: [
    { department: "Information Technology" },
    { department: "Finance" }
  ]
})
```

### Complex Logical Combinations
```javascript
// (IT OR Finance) AND (Salary > 60000) AND Active
db.employees.find({
  $and: [
    {
      $or: [
        { department: "Information Technology" },
        { department: "Finance" }
      ]
    },
    { salary: { $gt: 60000 } },
    { status: "Active" }
  ]
})

// Senior positions OR (IT department AND Salary > 70000)
db.employees.find({
  $or: [
    { position: { $regex: /Senior|Manager/, $options: "i" } },
    {
      $and: [
        { department: "Information Technology" },
        { salary: { $gt: 70000 } }
      ]
    }
  ]
})
```

---

## AGGREGATION PIPELINES

### COUNT Operations

#### Basic Count
```javascript
// Count all employees
db.employees.countDocuments()

// Count active employees
db.employees.countDocuments({ status: "Active" })

// Count IT department employees
db.employees.countDocuments({ department: "Information Technology" })

// Count pending leaves
db.leaves.countDocuments({ status: "Pending" })
```

#### Count with Aggregation
```javascript
// Count employees by department
db.employees.aggregate([
  {
    $group: {
      _id: "$department",
      count: { $sum: 1 }
    }
  },
  { $sort: { count: -1 } }
])

// Count leaves by status
db.leaves.aggregate([
  {
    $group: {
      _id: "$status",
      total: { $sum: 1 }
    }
  }
])

// Count employees by position
db.employees.aggregate([
  {
    $group: {
      _id: "$position",
      count: { $sum: 1 }
    }
  },
  { $sort: { count: -1 } }
])
```

---

### SUM Operations

```javascript
// Total salary expense
db.employees.aggregate([
  {
    $group: {
      _id: null,
      totalSalary: { $sum: "$salary" }
    }
  }
])

// Total salary by department
db.employees.aggregate([
  {
    $group: {
      _id: "$department",
      totalSalary: { $sum: "$salary" },
      employeeCount: { $sum: 1 }
    }
  },
  { $sort: { totalSalary: -1 } }
])

// Total salary paid (from salaries collection)
db.salaries.aggregate([
  {
    $group: {
      _id: null,
      totalBaseSalary: { $sum: "$base_salary" },
      totalAllowances: { $sum: "$allowances" },
      totalDeductions: { $sum: "$deductions" },
      totalNetSalary: { $sum: "$net_salary" }
    }
  }
])

// Total salary by month and year
db.salaries.aggregate([
  {
    $group: {
      _id: { year: "$year", month: "$month" },
      totalPaid: { $sum: "$net_salary" }
    }
  },
  { $sort: { "_id.year": -1, "_id.month": -1 } }
])
```

---

### AVERAGE (AVG) Operations

```javascript
// Average salary across all employees
db.employees.aggregate([
  {
    $group: {
      _id: null,
      averageSalary: { $avg: "$salary" }
    }
  }
])

// Average salary by department
db.employees.aggregate([
  {
    $group: {
      _id: "$department",
      averageSalary: { $avg: "$salary" },
      employeeCount: { $sum: 1 }
    }
  },
  { $sort: { averageSalary: -1 } }
])

// Average salary by position
db.employees.aggregate([
  {
    $group: {
      _id: "$position",
      avgSalary: { $avg: "$salary" },
      minSalary: { $min: "$salary" },
      maxSalary: { $max: "$salary" }
    }
  }
])

// Average net salary by year
db.salaries.aggregate([
  {
    $group: {
      _id: "$year",
      avgNetSalary: { $avg: "$net_salary" },
      avgAllowances: { $avg: "$allowances" },
      avgDeductions: { $avg: "$deductions" }
    }
  }
])
```

---

### MIN and MAX Operations

```javascript
// Minimum and maximum salary
db.employees.aggregate([
  {
    $group: {
      _id: null,
      minSalary: { $min: "$salary" },
      maxSalary: { $max: "$salary" },
      avgSalary: { $avg: "$salary" }
    }
  }
])

// Min/Max salary by department
db.employees.aggregate([
  {
    $group: {
      _id: "$department",
      minSalary: { $min: "$salary" },
      maxSalary: { $max: "$salary" },
      salaryRange: { $subtract: [{ $max: "$salary" }, { $min: "$salary" }] }
    }
  }
])

// Earliest and latest join dates
db.employees.aggregate([
  {
    $group: {
      _id: null,
      earliestJoinDate: { $min: "$join_date" },
      latestJoinDate: { $max: "$join_date" }
    }
  }
])
```

---

### MATCH (Filtering in Aggregation)

```javascript
// Average salary of IT employees only
db.employees.aggregate([
  { $match: { department: "Information Technology" } },
  {
    $group: {
      _id: null,
      avgSalary: { $avg: "$salary" },
      totalEmployees: { $sum: 1 }
    }
  }
])

// Count approved leaves per employee
db.leaves.aggregate([
  { $match: { status: "Approved" } },
  {
    $group: {
      _id: "$emp_id",
      approvedLeaves: { $sum: 1 }
    }
  },
  { $sort: { approvedLeaves: -1 } }
])

// Salary statistics for high earners (>70000)
db.employees.aggregate([
  { $match: { salary: { $gt: 70000 } } },
  {
    $group: {
      _id: "$department",
      count: { $sum: 1 },
      avgSalary: { $avg: "$salary" }
    }
  }
])
```

---

### PROJECT (Field Selection in Aggregation)

```javascript
// Show specific fields with calculations
db.employees.aggregate([
  {
    $project: {
      _id: 0,
      name: 1,
      department: 1,
      salary: 1,
      annualSalary: { $multiply: ["$salary", 12] }
    }
  }
])

// Calculate age from date of birth
db.employees.aggregate([
  {
    $project: {
      name: 1,
      department: 1,
      date_of_birth: 1,
      birthYear: { $substr: ["$date_of_birth", 0, 4] }
    }
  }
])
```

---

### SORT in Aggregation

```javascript
// Top 5 highest paid employees
db.employees.aggregate([
  { $sort: { salary: -1 } },
  { $limit: 5 },
  {
    $project: {
      _id: 0,
      name: 1,
      department: 1,
      position: 1,
      salary: 1
    }
  }
])

// Department-wise salary totals (sorted)
db.employees.aggregate([
  {
    $group: {
      _id: "$department",
      totalSalary: { $sum: "$salary" },
      avgSalary: { $avg: "$salary" },
      count: { $sum: 1 }
    }
  },
  { $sort: { totalSalary: -1 } }
])
```

---

### LIMIT and SKIP

```javascript
// Top 10 employees by salary
db.employees.aggregate([
  { $sort: { salary: -1 } },
  { $limit: 10 }
])

// Pagination - Page 2 (skip 10, limit 10)
db.employees.aggregate([
  { $sort: { emp_id: 1 } },
  { $skip: 10 },
  { $limit: 10 }
])
```

---

### Complex Aggregation Examples

```javascript
// Comprehensive employee statistics by department
db.employees.aggregate([
  {
    $group: {
      _id: "$department",
      totalEmployees: { $sum: 1 },
      totalSalaryExpense: { $sum: "$salary" },
      avgSalary: { $avg: "$salary" },
      minSalary: { $min: "$salary" },
      maxSalary: { $max: "$salary" },
      employees: { $push: "$name" }
    }
  },
  { $sort: { totalSalaryExpense: -1 } }
])

// Leave statistics by employee
db.leaves.aggregate([
  {
    $group: {
      _id: "$emp_id",
      totalLeaves: { $sum: 1 },
      approvedLeaves: {
        $sum: { $cond: [{ $eq: ["$status", "Approved"] }, 1, 0] }
      },
      pendingLeaves: {
        $sum: { $cond: [{ $eq: ["$status", "Pending"] }, 1, 0] }
      },
      rejectedLeaves: {
        $sum: { $cond: [{ $eq: ["$status", "Rejected"] }, 1, 0] }
      }
    }
  },
  { $sort: { totalLeaves: -1 } }
])

// Monthly salary expense trends
db.salaries.aggregate([
  {
    $group: {
      _id: { year: "$year", month: "$month" },
      totalBaseSalary: { $sum: "$base_salary" },
      totalAllowances: { $sum: "$allowances" },
      totalDeductions: { $sum: "$deductions" },
      totalNetSalary: { $sum: "$net_salary" },
      employeesPaid: { $sum: 1 }
    }
  },
  { $sort: { "_id.year": -1, "_id.month": -1 } }
])
```

---

## SORTING & LIMITING

### Simple Sorting

```javascript
// Sort by salary (ascending)
db.employees.find().sort({ salary: 1 })

// Sort by salary (descending)
db.employees.find().sort({ salary: -1 })

// Sort by name (alphabetically)
db.employees.find().sort({ name: 1 })

// Sort by join_date (newest first)
db.employees.find().sort({ join_date: -1 })
```

### Multi-field Sorting

```javascript
// Sort by department, then by salary (descending)
db.employees.find().sort({ 
  department: 1, 
  salary: -1 
})

// Sort by status, then by join date
db.employees.find().sort({ 
  status: 1, 
  join_date: -1 
})
```

### Limiting Results

```javascript
// Get top 5 highest paid employees
db.employees.find().sort({ salary: -1 }).limit(5)

// Get 10 most recent employees
db.employees.find().sort({ join_date: -1 }).limit(10)

// Get first 20 employees
db.employees.find().limit(20)
```

### Skip and Limit (Pagination)

```javascript
// Page 1 (first 10 records)
db.employees.find().sort({ emp_id: 1 }).limit(10)

// Page 2 (skip 10, next 10 records)
db.employees.find().sort({ emp_id: 1 }).skip(10).limit(10)

// Page 3 (skip 20, next 10 records)
db.employees.find().sort({ emp_id: 1 }).skip(20).limit(10)
```

---

## PROJECTION (FIELD SELECTION)

### Include Specific Fields

```javascript
// Show only name and salary
db.employees.find(
  {},
  { name: 1, salary: 1 }
)
// Note: _id is included by default

// Show name, email, department (exclude _id)
db.employees.find(
  {},
  { name: 1, email: 1, department: 1, _id: 0 }
)
```

### Exclude Specific Fields

```javascript
// Show all fields except salary
db.employees.find(
  {},
  { salary: 0 }
)

// Show all fields except password
db.users.find(
  {},
  { password: 0 }
)
```

### Projection with Conditions

```javascript
// IT employees - show only name and salary
db.employees.find(
  { department: "Information Technology" },
  { name: 1, salary: 1, _id: 0 }
)

// High earners - show name, position, salary
db.employees.find(
  { salary: { $gt: 70000 } },
  { name: 1, position: 1, salary: 1, _id: 0 }
)
```

---

## DATE & TIME QUERIES

### Date Comparisons

```javascript
// Employees who joined in 2024
db.employees.find({
  join_date: {
    $gte: new Date("2024-01-01"),
    $lt: new Date("2025-01-01")
  }
})

// Employees who joined after Jan 1, 2023
db.employees.find({
  join_date: { $gte: new Date("2023-01-01") }
})

// Leaves applied in last 30 days
db.leaves.find({
  applied_date: {
    $gte: new Date(Date.now() - 30*24*60*60*1000)
  }
})
```

### Date Range Queries

```javascript
// Salaries paid between two dates
db.salaries.find({
  pay_date: {
    $gte: new Date("2024-01-01"),
    $lte: new Date("2024-12-31")
  }
})

// Leaves for December 2024
db.leaves.find({
  start_date: { $gte: "2024-12-01", $lte: "2024-12-31" }
})
```

### Extract Date Parts

```javascript
// Employees who joined in a specific year
db.employees.aggregate([
  {
    $project: {
      name: 1,
      join_date: 1,
      joinYear: { $year: "$join_date" },
      joinMonth: { $month: "$join_date" }
    }
  },
  {
    $match: { joinYear: 2024 }
  }
])

// Group salaries by month
db.salaries.aggregate([
  {
    $group: {
      _id: { 
        year: { $year: "$pay_date" },
        month: { $month: "$pay_date" }
      },
      total: { $sum: "$net_salary" }
    }
  }
])
```

### Current Date Queries

```javascript
// Leaves applied today
db.leaves.find({
  applied_date: {
    $gte: new Date(new Date().setHours(0, 0, 0, 0)),
    $lt: new Date(new Date().setHours(23, 59, 59, 999))
  }
})
```

---

## ARRAY & STRING OPERATIONS

### String Pattern Matching (REGEX)

```javascript
// Names starting with 'S'
db.employees.find({
  name: { $regex: /^S/, $options: "i" }
})

// Emails containing 'company.com'
db.employees.find({
  email: { $regex: /company\.com$/, $options: "i" }
})

// Positions containing 'Engineer'
db.employees.find({
  position: { $regex: /Engineer/, $options: "i" }
})

// Names containing 'John' (case-insensitive)
db.employees.find({
  name: { $regex: /john/i }
})

// Phone numbers starting with '017'
db.employees.find({
  phone: { $regex: /^017/ }
})
```

### String Operations in Aggregation

```javascript
// Convert name to uppercase
db.employees.aggregate([
  {
    $project: {
      name: 1,
      upperName: { $toUpper: "$name" },
      lowerName: { $toLower: "$name" }
    }
  }
])

// Concatenate fields
db.employees.aggregate([
  {
    $project: {
      fullInfo: {
        $concat: ["$name", " - ", "$position", " (", "$department", ")"]
      }
    }
  }
])

// Extract substring
db.employees.aggregate([
  {
    $project: {
      name: 1,
      birthYear: { $substr: ["$date_of_birth", 0, 4] }
    }
  }
])
```

### Text Search

```javascript
// First create a text index
db.employees.createIndex({ name: "text", position: "text" })

// Search for 'engineer'
db.employees.find({
  $text: { $search: "engineer" }
})

// Search with multiple terms
db.employees.find({
  $text: { $search: "software senior" }
})
```

---

## JOIN OPERATIONS ($lookup)

### Basic Join

```javascript
// Join employees with their leave records
db.employees.aggregate([
  {
    $lookup: {
      from: "leaves",
      localField: "emp_id",
      foreignField: "emp_id",
      as: "leave_records"
    }
  },
  {
    $project: {
      name: 1,
      department: 1,
      totalLeaves: { $size: "$leave_records" },
      leave_records: 1
    }
  }
])
```

### Join with Filtering

```javascript
// Join employees with their salary records
db.employees.aggregate([
  {
    $lookup: {
      from: "salaries",
      localField: "emp_id",
      foreignField: "emp_id",
      as: "salary_history"
    }
  },
  {
    $match: { department: "Information Technology" }
  },
  {
    $project: {
      name: 1,
      department: 1,
      current_salary: "$salary",
      totalSalaryRecords: { $size: "$salary_history" }
    }
  }
])
```

### Multiple Joins

```javascript
// Join employees with leaves and salaries
db.employees.aggregate([
  {
    $lookup: {
      from: "leaves",
      localField: "emp_id",
      foreignField: "emp_id",
      as: "leaves"
    }
  },
  {
    $lookup: {
      from: "salaries",
      localField: "emp_id",
      foreignField: "emp_id",
      as: "salaries"
    }
  },
  {
    $project: {
      name: 1,
      department: 1,
      totalLeaves: { $size: "$leaves" },
      totalSalaryRecords: { $size: "$salaries" }
    }
  }
])
```

### Join with Department

```javascript
// Join employees with their department details
db.employees.aggregate([
  {
    $lookup: {
      from: "departments",
      localField: "department",
      foreignField: "name",
      as: "dept_info"
    }
  },
  {
    $unwind: "$dept_info"
  },
  {
    $project: {
      name: 1,
      position: 1,
      department: 1,
      dept_manager: "$dept_info.manager",
      dept_description: "$dept_info.description"
    }
  }
])
```

### Advanced Join with Pipeline

```javascript
// Join and count approved leaves only
db.employees.aggregate([
  {
    $lookup: {
      from: "leaves",
      let: { emp_id: "$emp_id" },
      pipeline: [
        {
          $match: {
            $expr: { $eq: ["$emp_id", "$$emp_id"] },
            status: "Approved"
          }
        }
      ],
      as: "approved_leaves"
    }
  },
  {
    $project: {
      name: 1,
      department: 1,
      approvedLeaveCount: { $size: "$approved_leaves" }
    }
  },
  { $sort: { approvedLeaveCount: -1 } }
])
```

---

## DISTRIBUTED DATABASE QUERIES

### Queries Across Multiple Databases

#### Query ems_db1 (Employee IDs 1-1000)
```javascript
// In MongoDB Compass, connect to ems_db1

// Find all employees in database 1
db.employees.find({ emp_id: { $lte: 1000 } })

// Count employees in this fragment
db.employees.countDocuments()

// Total salary expense in db1
db.employees.aggregate([
  {
    $group: {
      _id: null,
      totalSalary: { $sum: "$salary" },
      count: { $sum: 1 }
    }
  }
])
```

#### Query ems_db2 (Employee IDs 1001-2000)
```javascript
// In MongoDB Compass, connect to ems_db2

// Find all employees in database 2
db.employees.find({ 
  emp_id: { $gte: 1001, $lte: 2000 } 
})

// Department distribution in db2
db.employees.aggregate([
  {
    $group: {
      _id: "$department",
      count: { $sum: 1 }
    }
  }
])
```

#### Query ems_db3 (Employee IDs 2001-3000)
```javascript
// In MongoDB Compass, connect to ems_db3

// Find all employees in database 3
db.employees.find({ 
  emp_id: { $gte: 2001, $lte: 3000 } 
})

// Average salary in db3
db.employees.aggregate([
  {
    $group: {
      _id: null,
      avgSalary: { $avg: "$salary" }
    }
  }
])
```

---

### Replication Queries (Same Data Across All DBs)

```javascript
// Query departments (should return same data in all 3 DBs)
db.departments.find()

// Query users (replicated across all DBs)
db.users.find({ role: "employee" })

// Count departments in each database (should be same)
db.departments.countDocuments()
```

---

### Derived Fragmentation Queries

```javascript
// In ems_db1: Leaves for employees 1-1000
db.leaves.find({ emp_id: { $lte: 1000 } })

// In ems_db2: Salaries for employees 1001-2000
db.salaries.find({ 
  emp_id: { $gte: 1001, $lte: 2000 } 
})

// In ems_db3: Leaves for employees 2001-3000
db.leaves.find({ 
  emp_id: { $gte: 2001, $lte: 3000 } 
})
```

---

### Cross-Database Statistics

```javascript
// To get total employees across all databases, run in each DB:

// ems_db1
db.employees.countDocuments()  // Result: X

// ems_db2
db.employees.countDocuments()  // Result: Y

// ems_db3
db.employees.countDocuments()  // Result: Z

// Total = X + Y + Z
```

---

## INDEX OPERATIONS

### Create Indexes

```javascript
// Create index on emp_id (most common query field)
db.employees.createIndex({ emp_id: 1 })

// Create index on department
db.employees.createIndex({ department: 1 })

// Create compound index
db.employees.createIndex({ 
  department: 1, 
  salary: -1 
})

// Create index on email (unique)
db.employees.createIndex({ email: 1 }, { unique: true })

// Create text index for searching
db.employees.createIndex({ 
  name: "text", 
  position: "text" 
})

// Create index on leave status
db.leaves.createIndex({ status: 1 })

// Create index on salary date
db.salaries.createIndex({ pay_date: -1 })
```

### View Indexes

```javascript
// List all indexes on employees collection
db.employees.getIndexes()

// List indexes on leaves
db.leaves.getIndexes()
```

### Drop Indexes

```javascript
// Drop specific index
db.employees.dropIndex("department_1")

// Drop all indexes except _id
db.employees.dropIndexes()
```

### Explain Query (Performance Analysis)

```javascript
// Analyze query performance
db.employees.find({ 
  department: "Information Technology" 
}).explain("executionStats")

// Check if index is used
db.employees.find({ 
  emp_id: 105 
}).explain("executionStats")
```

---

## PRACTICE QUESTIONS

### Easy Level

1. **Find all employees**
```javascript
db.employees.find()
```

2. **Count total departments**
```javascript
db.departments.countDocuments()
```

3. **Find employees with salary > 60000**
```javascript
db.employees.find({ salary: { $gt: 60000 } })
```

4. **Find all pending leaves**
```javascript
db.leaves.find({ status: "Pending" })
```

5. **Sort employees by name**
```javascript
db.employees.find().sort({ name: 1 })
```

---

### Medium Level

6. **Find IT employees with salary between 50000 and 80000**
```javascript
db.employees.find({
  department: "Information Technology",
  salary: { $gte: 50000, $lte: 80000 }
})
```

7. **Count employees in each department**
```javascript
db.employees.aggregate([
  {
    $group: {
      _id: "$department",
      count: { $sum: 1 }
    }
  },
  { $sort: { count: -1 } }
])
```

8. **Find top 5 highest paid employees**
```javascript
db.employees.find().sort({ salary: -1 }).limit(5)
```

9. **Calculate average salary by department**
```javascript
db.employees.aggregate([
  {
    $group: {
      _id: "$department",
      avgSalary: { $avg: "$salary" },
      minSalary: { $min: "$salary" },
      maxSalary: { $max: "$salary" }
    }
  }
])
```

10. **Find employees who joined in 2023**
```javascript
db.employees.find({
  join_date: {
    $gte: new Date("2023-01-01"),
    $lt: new Date("2024-01-01")
  }
})
```

---

### Hard Level

11. **Find departments with more than 2 employees**
```javascript
db.employees.aggregate([
  {
    $group: {
      _id: "$department",
      count: { $sum: 1 }
    }
  },
  {
    $match: { count: { $gt: 2 } }
  }
])
```

12. **Calculate total salary expense and average per employee for each department**
```javascript
db.employees.aggregate([
  {
    $group: {
      _id: "$department",
      totalExpense: { $sum: "$salary" },
      avgSalary: { $avg: "$salary" },
      employeeCount: { $sum: 1 }
    }
  },
  {
    $project: {
      department: "$_id",
      totalExpense: 1,
      avgSalary: 1,
      employeeCount: 1,
      expensePerEmployee: { 
        $divide: ["$totalExpense", "$employeeCount"] 
      }
    }
  },
  { $sort: { totalExpense: -1 } }
])
```

13. **Find employees with approved leaves count**
```javascript
db.employees.aggregate([
  {
    $lookup: {
      from: "leaves",
      let: { emp_id: "$emp_id" },
      pipeline: [
        {
          $match: {
            $expr: { $eq: ["$emp_id", "$$emp_id"] },
            status: "Approved"
          }
        }
      ],
      as: "approved_leaves"
    }
  },
  {
    $project: {
      name: 1,
      department: 1,
      approvedLeaveCount: { $size: "$approved_leaves" }
    }
  },
  { $sort: { approvedLeaveCount: -1 } }
])
```

14. **Find employees with no leaves**
```javascript
db.employees.aggregate([
  {
    $lookup: {
      from: "leaves",
      localField: "emp_id",
      foreignField: "emp_id",
      as: "leaves"
    }
  },
  {
    $match: { leaves: { $size: 0 } }
  },
  {
    $project: {
      name: 1,
      department: 1,
      position: 1
    }
  }
])
```

15. **Monthly salary trends with statistics**
```javascript
db.salaries.aggregate([
  {
    $group: {
      _id: { 
        year: "$year", 
        month: "$month" 
      },
      totalBaseSalary: { $sum: "$base_salary" },
      totalAllowances: { $sum: "$allowances" },
      totalDeductions: { $sum: "$deductions" },
      totalNetSalary: { $sum: "$net_salary" },
      avgNetSalary: { $avg: "$net_salary" },
      employeesPaid: { $sum: 1 }
    }
  },
  {
    $project: {
      year: "$_id.year",
      month: "$_id.month",
      totalBaseSalary: 1,
      totalAllowances: 1,
      totalDeductions: 1,
      totalNetSalary: 1,
      avgNetSalary: 1,
      employeesPaid: 1,
      avgPerEmployee: { 
        $divide: ["$totalNetSalary", "$employeesPaid"] 
      }
    }
  },
  { $sort: { "_id.year": -1, "_id.month": -1 } }
])
```

---

## QUICK REFERENCE CHEAT SHEET

### Query Operators
```
Comparison:
  $eq   - Equal to
  $ne   - Not equal to
  $gt   - Greater than
  $gte  - Greater than or equal
  $lt   - Less than
  $lte  - Less than or equal
  $in   - In array
  $nin  - Not in array

Logical:
  $and  - AND condition
  $or   - OR condition
  $not  - NOT condition
  $nor  - NOR condition

Element:
  $exists - Field exists
  $type   - Field type check
```

### Aggregation Operators
```
Accumulator:
  $sum    - Sum values
  $avg    - Average
  $min    - Minimum
  $max    - Maximum
  $count  - Count documents
  $push   - Array of values
  $addToSet - Unique values

Pipeline Stages:
  $match    - Filter documents
  $group    - Group by field
  $project  - Select fields
  $sort     - Sort documents
  $limit    - Limit results
  $skip     - Skip documents
  $lookup   - Join collections
  $unwind   - Deconstruct array
```

### String Operators
```
  $regex  - Pattern matching
  $concat - Concatenate strings
  $substr - Substring
  $toUpper - Uppercase
  $toLower - Lowercase
```

### Date Operators
```
  $year   - Extract year
  $month  - Extract month
  $day    - Extract day
  $hour   - Extract hour
  $minute - Extract minute
```

---

## EXAM TIPS

### Common Query Patterns

1. **Always start simple, then add complexity**
2. **Use `.pretty()` for readable output**
3. **Test queries on small datasets first**
4. **Use aggregation for calculations**
5. **Remember projection to show only needed fields**
6. **Sort results for better presentation**
7. **Use indexes for performance questions**

### MongoDB Compass Tips

1. **Filter Box**: Use JSON queries directly
2. **Aggregation Tab**: Visual pipeline builder
3. **Schema Tab**: See field distributions
4. **Explain Plan**: Check query performance
5. **Export Results**: Save query outputs

### Common Mistakes to Avoid

1. ❌ Forgetting to specify database name
2. ❌ Using == instead of $eq in queries
3. ❌ Forgetting quotes around strings
4. ❌ Not checking data types (Number vs String)
5. ❌ Mixing up $match and find()
6. ❌ Forgetting to sort before limit
7. ❌ Using wrong collection name

---

## GOOD LUCK WITH YOUR EXAM! 🎓

**Remember:**
- Practice these queries in MongoDB Compass
- Understand the logic, don't just memorize
- Test variations of each query
- Explain your queries clearly
- Check results make sense

**Your project demonstrates:**
✅ Horizontal Fragmentation (3 databases)
✅ Data Replication (departments, users)
✅ Derived Fragmentation (leaves, salaries)
✅ Complex aggregations
✅ Real-world use cases

**You're well prepared! 💪**
