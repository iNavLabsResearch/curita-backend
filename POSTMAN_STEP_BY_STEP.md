# Step-by-Step Postman Guide for Beginners

## Part 1: Setup Postman

### Step 1: Install Postman (if you don't have it)
1. Go to: https://www.postman.com/downloads/
2. Download Postman for your operating system
3. Install it
4. Open Postman
5. Sign up for a free account (or sign in if you have one)

---

## Part 2: Start Your Backend Server

### Step 2: Start the Server
1. Open terminal/command prompt
2. Navigate to your project folder:
   ```bash
   cd /home/harshi/Desktop/Intership/curita-backend
   ```
3. Start the server:
   ```bash
   python main.py
   ```
4. Wait until you see: `✅ Application startup complete`
5. Server is running on: `http://localhost:8000`

**⚠️ Keep this terminal window open while testing!**

---

## Part 3: Create Your First Collection in Postman

### Step 3: Create a New Collection
1. Open Postman
2. Click the **"New"** button (top left)
3. Select **"Collection"**
4. Name it: **"Curita Backend API Tests"**
5. Click **"Create"**

### Step 4: Set Collection Variables
1. Right-click on your collection name
2. Click **"Edit"**
3. Go to the **"Variables"** tab
4. Add a new variable:
   - **Variable:** `base_url`
   - **Initial Value:** `http://localhost:8000/api/v1`
   - **Current Value:** `http://localhost:8000/api/v1`
5. Click **"Save"**

Now you can use `{{base_url}}` in all your requests!

---

## Part 4: Test Your First API (Health Check)

### Step 5: Create Health Check Request
1. Click the **"+"** button in Postman (or press `Ctrl+N` / `Cmd+N`)
2. You'll see a new request tab
3. Set the method to **GET** (dropdown on the left, should already be GET)
4. In the URL bar, type: `{{base_url}}/health`
5. Click **"Send"** button (blue button on the right)
6. You should see a response like:
   ```json
   {
     "status": "healthy",
     "service": "Curita RAG Backend"
   }
   ```

**✅ If you see this, your server is working!**

### Step 6: Save the Request
1. Click **"Save"** button (top right)
2. Type name: `Health Check`
3. Select your collection: **"Curita Backend API Tests"**
4. Click **"Save"**

---

## Part 5: Test CRUD Operations - Step by Step

### A. CREATE A TOY (POST Request)

#### Step 7: Create Toy Request
1. Click **"New"** → **"HTTP Request"**
2. Set method to **POST** (change dropdown from GET to POST)
3. URL: `{{base_url}}/toys`
4. Click **"Body"** tab (below URL bar)
5. Select **"raw"**
6. Select **"JSON"** from dropdown (right side)
7. Paste this JSON:
   ```json
   {
     "name": "My First Toy",
     "description": "A test toy",
     "is_active": true
   }
   ```
8. Click **"Send"**
9. You should get a response with the created toy including an `id`
10. **Copy the `id` from the response** - you'll need it later!
11. Click **"Save"** → Name: `Create Toy` → Save to collection

**📝 Example Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "My First Toy",
  "description": "A test toy",
  "is_active": true,
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

---

### B. LIST ALL TOYS (GET Request)

#### Step 8: List Toys Request
1. Click **"New"** → **"HTTP Request"**
2. Method: **GET**
3. URL: `{{base_url}}/toys`
4. Click **"Send"**
5. You should see an array of toys
6. Save as: `List All Toys`

---

### C. GET TOY BY ID (GET Request)

#### Step 9: Get Single Toy Request
1. Click **"New"** → **"HTTP Request"**
2. Method: **GET**
3. URL: `{{base_url}}/toys/YOUR_TOY_ID_HERE`
   - Replace `YOUR_TOY_ID_HERE` with the ID you copied from Step 7
   - Example: `{{base_url}}/toys/123e4567-e89b-12d3-a456-426614174000`
4. Click **"Send"**
5. You should see the toy details
6. Save as: `Get Toy by ID`

---

### D. UPDATE TOY (PUT Request)

#### Step 10: Update Toy Request
1. Click **"New"** → **"HTTP Request"**
2. Method: **PUT**
3. URL: `{{base_url}}/toys/YOUR_TOY_ID_HERE` (use your toy ID)
4. Click **"Body"** tab
5. Select **"raw"** and **"JSON"**
6. Paste this:
   ```json
   {
     "name": "Updated Toy Name",
     "description": "Updated description"
   }
   ```
7. Click **"Send"**
8. You should see the updated toy
9. Save as: `Update Toy`

---

### E. DELETE TOY (DELETE Request)

#### Step 11: Delete Toy Request
1. Click **"New"** → **"HTTP Request"**
2. Method: **DELETE**
3. URL: `{{base_url}}/toys/YOUR_TOY_ID_HERE` (use your toy ID)
4. Click **"Send"**
5. You should see:
   ```json
   {
     "success": true,
     "message": "Toy deleted successfully"
   }
   ```
6. Save as: `Delete Toy`

---

## Part 6: Test More Complex Operations

### F. CREATE A PROVIDER (POST Request)

#### Step 12: Create Model Provider
1. New Request
2. Method: **POST**
3. URL: `{{base_url}}/providers/models`
4. Body → raw → JSON:
   ```json
   {
     "provider_name": "openai",
     "model_name": "gpt-4",
     "is_large_model": true,
     "default_temperature": 0.7,
     "supported_languages": ["en"],
     "is_default": true
   }
   ```
5. Send and save as: `Create Model Provider`

---

### G. CREATE AN AGENT (POST Request)

#### Step 13: Create Agent
1. New Request
2. Method: **POST**
3. URL: `{{base_url}}/agents`
4. Body → raw → JSON:
   ```json
   {
     "toy_id": "YOUR_TOY_ID_HERE",
     "name": "Assistant Agent",
     "system_prompt": "You are a helpful assistant",
     "language_code": "en-US",
     "is_active": true
   }
   ```
   **Replace `YOUR_TOY_ID_HERE` with an actual toy ID!**
5. Send and save as: `Create Agent`

---

## Part 7: Organize Your Requests

### Step 14: Create Folders in Collection
1. Right-click on your collection
2. Click **"Add Folder"**
3. Name it: **"Toys"**
4. Repeat for:
   - **"Providers"**
   - **"Agents"**
   - **"Tools"**
   - **"Memory"**

### Step 15: Move Requests to Folders
1. Drag and drop requests into appropriate folders:
   - `Create Toy`, `List All Toys`, `Get Toy by ID`, etc. → **Toys** folder
   - `Create Model Provider` → **Providers** folder
   - `Create Agent` → **Agents** folder

---

## Part 8: Testing Checklist

### Quick Testing Flow:

#### ✅ 1. Health Check
- [ ] GET `{{base_url}}/health` - Should return "healthy"

#### ✅ 2. Providers
- [ ] POST `{{base_url}}/providers/models` - Create model provider
- [ ] GET `{{base_url}}/providers/models` - List providers
- [ ] GET `{{base_url}}/providers/models/{id}` - Get one provider

#### ✅ 3. Toys
- [ ] POST `{{base_url}}/toys` - Create toy
- [ ] GET `{{base_url}}/toys` - List toys
- [ ] GET `{{base_url}}/toys/{id}` - Get one toy
- [ ] PUT `{{base_url}}/toys/{id}` - Update toy
- [ ] DELETE `{{base_url}}/toys/{id}` - Delete toy

#### ✅ 4. Agents
- [ ] POST `{{base_url}}/agents` - Create agent (need toy_id)
- [ ] GET `{{base_url}}/toys/{toy_id}/agents` - List agents for toy
- [ ] GET `{{base_url}}/agents/{agent_id}` - Get one agent
- [ ] PUT `{{base_url}}/agents/{agent_id}` - Update agent
- [ ] DELETE `{{base_url}}/agents/{agent_id}` - Delete agent

#### ✅ 5. Tools
- [ ] POST `{{base_url}}/tools` - Create tool (need toy_id)
- [ ] GET `{{base_url}}/toys/{toy_id}/tools` - List tools
- [ ] GET `{{base_url}}/tools/{tool_id}` - Get one tool
- [ ] PUT `{{base_url}}/tools/{tool_id}` - Update tool
- [ ] DELETE `{{base_url}}/tools/{tool_id}` - Delete tool

---

## Part 9: Common Issues and Solutions

### Issue 1: "Could not get any response"
**Solution:** 
- Check if your server is running (Step 2)
- Check the URL is correct: `http://localhost:8000/api/v1/health`

### Issue 2: "404 Not Found"
**Solution:**
- Check the URL path is correct
- Make sure you're using the right HTTP method (GET, POST, PUT, DELETE)
- Check if the resource ID exists

### Issue 3: "400 Bad Request"
**Solution:**
- Check your JSON body is valid (use a JSON validator)
- Make sure all required fields are included
- Check data types match (UUIDs should be strings, numbers should be numbers)

### Issue 4: "500 Internal Server Error"
**Solution:**
- Check server logs in your terminal
- Verify database connection
- Check if all required environment variables are set

---

## Part 10: Useful Postman Features

### Feature 1: Save Response IDs Automatically
1. Open a request (like "Create Toy")
2. Go to **"Tests"** tab
3. Add this code:
```javascript
if (pm.response.code === 201) {
    const response = pm.response.json();
    pm.collectionVariables.set("last_toy_id", response.id);
    console.log("Saved Toy ID:", response.id);
}
```
4. Now you can use `{{last_toy_id}}` in other requests!

### Feature 2: Test Response Status
In the **"Tests"** tab, add:
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```

### Feature 3: Pretty Print JSON
- Postman automatically formats JSON responses
- Look for the **"Pretty"** button in the response section

### Feature 4: View Response Time
- Check the response time at the bottom of the response panel
- Useful for performance testing

---

## Part 11: Complete Example Workflow

### Full CRUD Test for Toys:

1. **CREATE** → POST `{{base_url}}/toys`
   ```json
   {
     "name": "Test Toy",
     "description": "Testing",
     "is_active": true
   }
   ```
   - Copy the `id` from response

2. **READ (List)** → GET `{{base_url}}/toys`
   - Should see your toy in the list

3. **READ (One)** → GET `{{base_url}}/toys/{id}`
   - Should see your toy details

4. **UPDATE** → PUT `{{base_url}}/toys/{id}`
   ```json
   {
     "name": "Updated Test Toy"
   }
   ```

5. **DELETE** → DELETE `{{base_url}}/toys/{id}`
   - Should return success message

6. **VERIFY DELETE** → GET `{{base_url}}/toys/{id}`
   - Should return 404 Not Found

---

## Part 12: Visual Guide

### Postman Interface Explained:

```
┌─────────────────────────────────────────┐
│  New  Import  Collections  [Search]     │  ← Top Bar
├─────────────────────────────────────────┤
│  [GET ▼] [URL bar]              [Send]  │  ← Request Line
│  Params  Auth  Headers  Body  Pre-req   │  ← Tabs
│  Tests  Settings                        │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Body tab:                      │   │
│  │  ● raw  ○ form-data             │   │
│  │  [JSON ▼]                       │   │
│  │                                 │   │
│  │  {                              │   │
│  │    "name": "value"              │   │
│  │  }                              │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
         ↓ (Click Send)
┌─────────────────────────────────────────┐
│  Body  Cookies  Headers  Test Results   │  ← Response Tabs
│                                         │
│  {                                      │
│    "id": "123...",                     │
│    "name": "value",                    │
│    ...                                 │
│  }                                      │
│                                         │
│  Status: 200 OK  Time: 45ms            │  ← Status Bar
└─────────────────────────────────────────┘
```

---

## Summary: Your First 5 Minutes with Postman

1. ✅ Install Postman
2. ✅ Start your server (`python main.py`)
3. ✅ Create a collection named "Curita Backend API Tests"
4. ✅ Add variable: `base_url` = `http://localhost:8000/api/v1`
5. ✅ Test Health Check: GET `{{base_url}}/health`
6. ✅ Create a Toy: POST `{{base_url}}/toys` with JSON body
7. ✅ List Toys: GET `{{base_url}}/toys`
8. ✅ Get One Toy: GET `{{base_url}}/toys/{id}`
9. ✅ Update Toy: PUT `{{base_url}}/toys/{id}` with JSON body
10. ✅ Delete Toy: DELETE `{{base_url}}/toys/{id}`

**That's it! You've completed a full CRUD cycle! 🎉**

---

## Need More Help?

- Check server logs in your terminal for error messages
- Use Postman's Console: View → Show Postman Console (to see detailed request/response)
- Read the full API documentation at: `http://localhost:8000/docs` (Swagger UI)

**Happy Testing! 🚀**

