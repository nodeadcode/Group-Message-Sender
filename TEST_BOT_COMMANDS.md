# 🧪 Testing /generate and /redeem Commands

## Test Plan

### 1. Owner ID Verification
- ✅ OWNER_TELEGRAM_ID = 8395808382 (set in .env)
- ✅ Bot loads config from .env correctly

### 2. /generate Command (Owner Only)

**Test as Owner (ID: 8395808382):**
```
/generate weekly
Expected: ✅ Generate code for ₹99/7 days

/generate monthly  
Expected: ✅ Generate code for ₹299/30 days
```

**Test as Non-Owner:**
```
/generate weekly
Expected: ❌ "This command is only for the bot owner!"
```

### 3. /redeem Command (All Users)

**Test with Valid Code:**
```
/redeem ABC123XYZ
Expected: ✅ Activate subscription if code exists and unused
```

**Test with Invalid Code:**
```
/redeem INVALID
Expected: ❌ "Invalid code. Please check and try again."
```

**Test with Used Code:**
```
/redeem USED_CODE
Expected: ❌ "This code has already been used."
```

## Current Implementation Status

### ✅ Working Features:
1. Owner check on line 90: `if user_id != OWNER_TELEGRAM_ID`
2. Plan validation: Checks if plan_type in PLANS
3. Code generation: Unique 10-character codes
4. Database storage: AccessCode model with created_by
5. Code redemption: Full validation and subscription creation

### 🔧 Fixes Applied:
1. Fixed bot.py indentation (line 94)
2. Added better error messages
3. Added validation for plan types
4. Added db.refresh(owner) after commit

## How to Test:

1. **Start the bot:**
   ```bash
   cd bot
   python bot.py
   ```

2. **As owner (8395808382), try:**
   ```
   /generate weekly
   ```

3. **As any user, try:**
   ```
   /redeem CODE_FROM_STEP2
   ```

4. **Verify in database:**
   ```bash
   cd backend
   python -c "from database import SessionLocal; from models import AccessCode, Subscription; db = SessionLocal(); print('Codes:', db.query(AccessCode).all()); print('Subs:', db.query(Subscription).all())"
   ```

## Expected Results:

✅ Owner can generate codes
✅ Non-owners get rejection message
✅ All users can redeem valid codes
✅ Subscriptions created correctly
✅ Codes marked as used after redemption
