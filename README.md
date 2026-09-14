# Habbo-Group-Manager
An advanced group management overlay for Habbo via G-Earth. Bypasses native client limitations by introducing multi-selection checkboxes, bulk operations, and mass member deletion.

## Features

* **Automatic Localization:** Interface language adapts automatically based on the connected host (Supports EN, PT, ES, FR, IT, DE, NL, FI, TR).
* **Real-time Asset Rendering:** Native rendering of group badges, member avatars, and administrative icons (Owner/Admin) directly from the game's XML/SWF assets.
* **Dynamic Pagination:** Strict state-managed pagination to prevent client freezing during large data queries.
* **Integrated Search:** Real-time user querying without requiring page reloads.
* **Bulk Operations:**
  * **Page Selection:** Target all rendered members simultaneously via checkboxes.
  * **Admin Rights Management:** Batch grant or revoke administrative privileges.
  * **Request Handling:** Batch accept pending membership requests or kick selected users.
* **Global Operations (Owner Only):**
  * **Global Accept:** Automates the approval of all pending requests sequentially across all pages.
  * **Global Wipe:** Automates the removal of all standard members (preserves Owner and Administrators).

## Interface & Role-Based Views

The interface dynamically adapts its control layout depending on the user's effective rank within the active group:

### 1. Owner View
Provides full administrative access, including global bulk actions (`Delete all members` and `Select all pending in group`), alongside standard batch management tools.



### 2. Admin View
Grants standard management controls such as batch member removal, admin rights management, and pending request handling, while restricting destructive global commands.



### 3. Member View
A clean, read-only layout restricted to browsing member information, viewing historical join dates, and navigating pagination without administrative overhead.



## Requirements

* [G-Earth](https://github.com/sirjonasxx/G-Earth/releases) (>= 1.4.1)
* Python 3.x
* Required Python packages: `g_python`, `Pillow`, `requests`

## Installation & Usage

1. Clone this repository and ensure the `images/` directory is located in the same path as the main script.
2. Install the required dependencies:
   ```bash
   pip install g_python Pillow requests
   ```
3. Launch G-Earth and connect to the game client.
4. Execute the extension via terminal:
    ```bash
    python enhanced_group_interface_1.0.py -p 9092
    ```
5. In the game client, open the Members tab of any group. The custom overlay interface will initialize and sync automatically.

## Critical Warnings

**Automated Global Operations:**
Global operations (Delete all members and Select all pending in group) iterate through all available pages via automated packet injection.
  * **Rate Limiting:** A deliberate delay (0.5s per action, 1.0s per page) is hardcoded to prevent connection drops due to packet flooding. Do not close the interface or the game client until the completion alert is triggered.
  * **Irreversible Actions:** The Delete all members function cannot be undone. It strictly ignores users with Owner (rank: 0) or Admin (rank: 1) status, but will permanently kick all standard members (rank: 2).
