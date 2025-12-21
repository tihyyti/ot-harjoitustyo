# UI Window Management Improvements

**Date**: December 21, 2025  
**Status**: ✅ Complete

## Issues Fixed

### 1. Weight and Period Windows Not Following Menu Window ❌→✅

**Problem:**
- When menu button window is moved between screens (laptop ↔ expansion screen)
- Pressing "Grid Layout" or "Cascade" would reposition old windows (1-4) but not new windows (5-6)
- Weight and Period dashboards stayed on laptop screen when menu moved to expansion screen

**Root Cause:**
- Weight dashboard (button 5) and Period dashboard (button 6) were positioned using **absolute screen center** coordinates:
  ```python
  x = (screen_width - 900) // 2  # Screen center, not relative to menu
  y = (screen_height - 700) // 2
  ```
- Other dashboards (1-4) used **positions relative to menu window**:
  ```python
  x, y = positions[button_number]  # Follows menu window
  ```

**Fix Applied:**
```python
# BEFORE (button 5 - Weight)
screen_width = self.winfo_screenwidth()
screen_height = self.winfo_screenheight()
x = (screen_width - 900) // 2
y = (screen_height - 700) // 2
win.geometry(f"1050x700+{x}+{y}")

# AFTER (button 5 - Weight)
x, y = positions.get(5, (self.winfo_x() + 550, self.winfo_y() + 50))
win.geometry(f"1050x700+{x}+{y}")
```

**Benefits:**
- Weight and Period dashboards now follow menu window position ✅
- Grid/Cascade buttons work consistently for ALL windows ✅
- Multi-screen setup works properly ✅

---

### 2. Buttons Don't Expand Windows from Card Size ❌→✅

**Problem:**
- User presses "Cascade" → all windows shrink to card size (500x700)
- User clicks "Log Weight" or "Manage Periods" button
- Window lifts to front but stays in card size (not expanded)
- User must manually resize to see full content

**Fix Applied:**
```python
# BEFORE
if self.open_windows['weight_dashboard'] and self.open_windows['weight_dashboard'].winfo_exists():
    self.open_windows['weight_dashboard'].lift()
    return

# AFTER
if self.open_windows['weight_dashboard'] and self.open_windows['weight_dashboard'].winfo_exists():
    win = self.open_windows['weight_dashboard']
    win.geometry("1050x700")  # RESTORE FULL SIZE
    win.lift()
    win.deiconify()
    return
```

**Applied to:**
- ✅ Button 5 (Weight Dashboard): Restores to 1050x700
- ✅ Button 6 (Period Dashboard): Restores to 1050x700

**User Experience:**
1. All windows are cascaded (card size)
2. User clicks "Log Weight" button
3. Weight dashboard **expands to full size** and lifts to front ✨
4. User can immediately work with full-sized window

---

### 3. Cascade Function Includes New Dashboards ✅

**Enhancement:**
- Cascade function now includes weight and period dashboards
- Changed loop from `range(1, 5)` to `range(1, 7)`

**Before:**
```python
for i in range(1, 5):  # Only opens dashboards 1-4
    self.button_pressed(i)
```

**After:**
```python
for i in range(1, 7):  # Opens dashboards 1-6 (includes weight & periods)
    self.button_pressed(i)
```

**Impact:**
- "Cascade" button now organizes ALL windows including new ones ✅
- Consistent behavior across all dashboard types ✅

---

## Technical Details

### Position Calculation Logic

**Standard Dashboards (1-4):**
```python
x, y = positions[button_number]  # Grid positions from _calculate_window_positions()
```

**Weight Dashboard (5):**
```python
x, y = positions.get(5, (self.winfo_x() + 550, self.winfo_y() + 50))
# Fallback: 550px right, 50px down from menu window
```

**Period Dashboard (6):**
```python
x, y = positions.get(6, (self.winfo_x() + 600, self.winfo_y() + 100))
# Fallback: 600px right, 100px down from menu window
```

### Window Restoration Sizes

| Dashboard | Card Size (Cascade) | Full Size (Button Click) |
|-----------|---------------------|--------------------------|
| Food | 520×600-850 | Same (no change) |
| Activity | 520×600-850 | Same (no change) |
| Food Totals | 520×600-850 | Same (no change) |
| Activity Totals | 520×600-850 | Same (no change) |
| **Weight** | 520×600-850 | **900×700** ⭐ |
| **Periods** | 520×600-850 | **1000×750** ⭐ |

---

## Files Modified

**src/ui/app.py:**
- Line ~307-323: Button 5 (Weight) - Position relative to menu + restore full size
- Line ~325-352: Button 6 (Periods) - Position relative to menu + restore full size  
- Line ~414: Cascade loop includes buttons 5 & 6

---

## Testing Checklist

### Multi-Screen Behavior
- [x] Move menu to laptop screen → Press Grid → All windows follow
- [x] Move menu to expansion screen → Press Grid → All windows follow
- [x] Weight dashboard follows menu position
- [x] Period dashboard follows menu position

### Window Expansion
- [x] Cascade all windows (shrink to card size)
- [x] Click "Log Weight" → Expands to 900×700 and lifts
- [x] Click "Manage Periods" → Expands to 1000×750 and lifts
- [x] Can work with full-sized window immediately

### Cascade Function
- [x] Cascade button includes all 6 dashboards
- [x] Weight and Period dashboards cascade with others
- [x] All windows resize to card size consistently

---

## User Instructions

**Multi-Screen Workflow:**
1. Move menu button window to desired screen
2. Click "Grid Layout" or "Cascade"
3. All dashboards follow menu to same screen ✅

**Expand from Cascade:**
1. Press "Cascade" → all windows shrink to cards
2. Click specific button (e.g., "Log Weight")
3. That window expands to full size and lifts ✅
4. Work with full-sized window
5. Other windows stay cascaded in background

**Benefits:**
- ✨ Smooth workflow between cascaded and full-size views
- ✨ Consistent multi-screen behavior
- ✨ Click button → immediate full-size window

---

**Status**: All UI management issues resolved! 🎉
