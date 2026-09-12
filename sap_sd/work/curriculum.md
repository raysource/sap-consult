# 视频内容摘录（deduped screens） 源: 录像45 Sales order processing.mp4

共 128 个不同画面（198 帧原始记录）。


## 1. [00:00-00:46] Unit 14: Sales Order Processing (slide)
- Unit 14: Sales Order Processing
- After completing this unit, you will be able to:
- Determine the origin of document data from various sources, like the material master, the customer master, or Customizing
- Find and use the tools and help for entering and processing sales orders
- NetMeeting
- Windows NetMeeting
- _(notes)_ Opening objective slide of the unit. Slides are played inside a Windows Internet Explorer window titled 'SAP Education'. The Windows taskbar is Chinese-localised (开始 / 控制面板) and also shows '3 Internet

## 2. [02:17-02:17] Overview: Sources for Document Data (slide)
- Overview: Sources for Document Data
- Information sources are:
- Master data
- Customer master / Material master / Conditions / ...
- Example: Customer master: Plant, shipping condition
- Example: Material master: Plant, loading group
- Existing document data
- Order
- Example: The delivering plant at item level as the basis for determining the shipping point
- Customizing
- IMG
- e.g. Sales document type: delivery block, shipping condition
- e.g. Determination of shipping point
- Hard-coded controls
- _(notes)_ Four-column diagram: master data, existing document data, Customizing and hard-coded ABAP controls each feed the order, with an 'Example' annotation under each column. The ABAP snippet text is small a

## 3. [06:03-06:45] Sales Order Entry - Deriving the Sales Area (slide)
- Sales Order Entry - Deriving the Sales Area
- Existing document data
- Order
- Customizing
- IMG
- e.g. Sales document type: delivery block, shipping condition
- e.g. Determination of shipping point
- Hard-coded controls
- ABAP
- Example: The delivering plant at item level as the basis for determining the shipping point
- Example: Weighting the different sources of information during plant determination
- Sold-to party C1 Smith Inc.
- Ship-to party S1 Smith Inc.
- Sales area: 1000 10 00
- _(notes)_ Mid-transition/animation frame: the slide TITLE has already switched to 'Sales Order Entry - Deriving the Sales Area' while the body still shows the previous slide's ('Overview: Sources for Document D

## 4. [06:48-06:48] SAP (logon screen) (gui)
- User System Help
- New password
- Client
- 800
- User
- Password
- ********
- Language
- SAP Training System
- Powered by .NET Microsoft Technology
- S000
- trn03
- OVR
- _(notes)_ SAP GUI for Windows logon screen (window titled 'SAP', menu bar 'User System Help'), system 'SAP Training System', client 800, user and language still empty - sign-on not yet executed. Status bar righ

## 5. [07:06-07:13] SAP Easy Access (gui)
- SAP Easy Access
- Menu Edit Favorites Extras System Help
- Favorites
- SAP menu
- Office
- Cross-Application Components
- Auto-ID Infrastructure
- Collaboration Projects
- Logistics
- Accounting
- Human Resources
- Information Systems
- S000
- trn03
- _(notes)_ SAP Easy Access right after logon: the tree is drawn but the right-hand pane is still rendering (logon-screen artwork still visible). Toolbar shows the standard buttons (Other menu, Create role, Assig

## 6. [07:26-07:26] SAP Easy Access (screen 'Create Sales Order: Initial Screen' not yet redrawn in the title area) (gui T-code=VA01)
- SAP Easy Access
- Menu Edit Favorites Extras System Help
- Create with Reference
- Sales
- Item overview
- Ordering party
- Order Type
- or
- Organizational data
- Sales Organization
- Distribution Channel
- Division
- Sales Office
- Sales Group
- _(notes)_ Initial screen of VA01 (Create Sales Order) called up from the Easy Access menu; the window/screen heading area still shows 'SAP Easy Access' while the screen body is the order-entry initial screen. A

## 7. [08:12-08:12] SAP (logon screen) (gui)
- User System Help
- New password
- Client
- 800
- User
- Password
- ********
- Language
- SAP Training System
- Powered by .NET Microsoft Technology
- S000
- trn03
- OVR
- _(notes)_ SAP GUI logon screen again (system 'SAP Training System', client 800) - the demo returns to the sign-on screen between takes. Appearance is partly ghosted/mid-refresh. Status bar right: S000 / trn03 /

## 8. [08:33-08:34] SAP Easy Access (gui)
- SAP Easy Access
- Menu Edit Favorites Extras System Help
- Favorites
- SAP menu
- Office
- Cross-Application Components
- Auto-ID Infrastructure
- Collaboration Projects
- Logistics
- Accounting
- Human Resources
- Information Systems
- Tools
- SESSION_MANAGER
- _(notes)_ SAP Easy Access after a fresh logon, now in the newer (Waves) SAP GUI theme. Standard Easy Access tree. Status bar right: SESSION_MANAGER / trn03 / OVR.

## 9. [08:37-08:37] Create Sales Order: Initial Screen (gui T-code=VA01)
- Sales document Edit Goto Environment System Help
- Create Sales Order: Initial Screen
- Create with Reference
- Sales
- Item overview
- Ordering party
- Order Type
- or
- Organizational data
- Sales Organization
- Distribution Channel
- Division
- Sales Office
- Sales Group
- _(notes)_ The VA01 initial screen now fully drawn and titled 'Create Sales Order: Initial Screen' with the sales-document menu bar. Enter-order-type field plus 'or' (with reference) field, empty Organizational 

## 10. [08:49-08:49] Create Standard Order: Overview (gui T-code=VA01)
- Sales document Edit Goto Extras Environment System Help
- Create Standard Order: Overview
- Orders
- Sales
- Item overview
- Item detail
- Ordering party
- Procurement
- Shipping
- Reason for rejection
- Standard Order
- Net value
- 0.00
- Sold-to party
- _(notes)_ Overview screen of the new order (order type Standard Order selected, hence the heading 'Create Standard Order: Overview'). Header fields filled with defaults only - sold-to/ship-to and PO data still 

## 11. [09:02-09:02] Create Standard Order: Overview (with popup 'Sales area for customer') (gui T-code=VA01)
- Create Standard Order: Overview
- Sales area for customer
- SOrg
- DC
- Dv
- Description
- 0001
- 01
- 01
- Sales Org. Germany / Direct Sales / Pumps
- 0001
- 01
- A1
- Sales Org. Germany / Direct Sales / Vehicles
- _(notes)_ Trainer enters sold-to party 1000; the 'Sales area for customer' selection dialog pops up listing the five valid sales areas for that customer, and the row 1000/10/00 Germany Frankfurt / Final custome

## 12. [09:17-09:17] Create Standard Order: Overview (with popup 'Partner selection') (gui T-code=VA01)
- Create Standard Order: Overview
- Partner selection
- Funct
- Name
- M
- P
- Partners
- Title
- Name 1
- SH
- Ship-to party
- Company
- Becker Berlin
- 0000001000
- _(notes)_ A 'Partner selection' dialog is open for the ship-to party function; two candidate partners for customer 1000 (Becker Berlin) are listed, one of them flagged with a red error/status indicator. Column 

## 13. [09:28-09:41] Create Standard Order: Overview (gui T-code=VA01)
- Create Standard Order: Overview
- Sales
- Item overview
- Item detail
- Ordering party
- Procurement
- Shipping
- Reason for rejection
- Standard Order
- Net value
- 0.00
- Sold-to party
- 1000
- Ship-to party
- _(notes)_ The PO Number field is highlighted in yellow and the system has returned the error/check message 'Enter PO number' in the status bar (red icon) - the field is mandatory for this order type. Status bar

## 14. [09:43-09:43] Sales Order Entry - Deriving the Sales Area (slide)
- Sales Order Entry - Deriving the Sales Area
- Order
- Sold-to party:   C1 Smith Inc.
- Ship-to party:   S1 Smith Inc.
- Sales area:   1000  10  00
- Item:  M1 Material 1
- Customer master
- C1 Smith Inc.
- _(notes)_ Slide rendered inside an Internet Explorer window (SAP Education banner); clock 14:01. Diagram shows the order fields on the left and the customer master record on the right, illustrating how the sale

## 15. [09:55-09:58] Proposing Order Data from Master Data (slide)
- Proposing Order Data from Master Data
- Customer master
- Business Partners
- Pricing
- Tax determination
- Delivery scheduling
- Payment
- Order
- Sold-to party:   C1
- Ship-to party:   W1
- Master data
- Customer-material info
- Output
- Item
- _(notes)_ Title-only build step of the slide: body still empty (animation just started); clock 14:02.

## 16. [12:35-12:35] Proposing Order Data from Master Data -> Create Standard Order: Overview (transition) (other)
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Orders
- Proposing Order Data from Master Data
- _(notes)_ Cross-fade frame between a slide and the live SAP GUI (both layers partly visible); not a clean slide or clean GUI screen. The SAP GUI menu bar and the 'Orders' toolbar button are already drawn while 

## 17. [12:36-12:37] Create Standard Order: Overview (gui T-code=VA01)
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Create Standard Order: Overview
- Orders
- Standard Order
- Net value
- 0.00 EUR
- Sold-to party
- 1000
- Becker Berlin
- Calvinstrasse 36
- 13467 Berlin-Hermsdorf
- Ship-to party
- 1000
- PO Number
- _(notes)_ Live SAP GUI, Create Standard Order overview screen; the outgoing slide still ghosts faintly over the window (transition in progress). Status bar shows VA01 | trn03 | OVR; clock 14:04.

## 18. [12:55-12:55] Create Standard Order: Overview with slide title overlaid (transition) (other T-code=VA01)
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Create Standard Order: Overview
- Proposing Order Data f
- Orders
- Standard Order
- Net value
- 0.00 EUR
- Sold-to party
- 1000
- Becker Berlin
- Calvinstrasse 36
- 13467 Berlin-Hermsdorf
- Ship-to party
- 1000
- _(notes)_ Cross-fade frame between a slide and the live SAP GUI (both layers partly visible); not a clean slide or clean GUI screen. The overview screen is fully legible underneath while the slide title 'Propos

## 19. [12:57-12:57] Proposing Order Data from Master Data (slide)
- Proposing Order Data from Master Data
- Customer master
- Business Partners
- Pricing
- Tax determination
- Delivery scheduling
- Payment
- Output
- Order
- Sold-to party:   C1
- Ship-to party:   W1
- Item
- Material
- Quantity
- _(notes)_ Full diagram slide shown again after the first GUI demo pass; clock 14:05.

## 20. [13:01-13:01] Business Partners from the Customer Master (slide)
- Business Partners from the Customer Master
- Sold-to party
- Ship-to party
- Bill-to party
- Payer
- Customer master
- _(notes)_ Simple diagram: the four partner roles (Sold-to party, Ship-to party, Bill-to party, Payer) all derive from the central Customer master record; clock 14:05.

## 21. [13:16-13:16] Business Partners from the Customer Master -> Create Standard Order: Overview (transition) (other T-code=VA01)
- Business Partners from the Customer Master
- Sold-to party
- Ship-to party
- Bill-to party
- Payer
- Customer master
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Create Standard Order: Overview
- Create Standard Order: Overview
- _(notes)_ Cross-fade frame between a slide and the live SAP GUI (both layers partly visible); not a clean slide or clean GUI screen. The SAP GUI window (title bar 'Create Standard Order: Overview') is opening o

## 22. [13:17-13:17] Create Standard Order: Overview (gui T-code=VA01)
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Create Standard Order: Overview
- Orders
- Standard Order
- Net value
- 0.00 EUR
- Sold-to party
- 1000
- Becker Berlin
- Calvinstrasse 36
- 13467 Berlin-Hermsdorf
- Ship-to party
- 1000
- PO Number
- _(notes)_ Clean overview screen used as the starting point for the partner/header demo; 'All items' grid empty with First date column pre-filled 09.06.2007. Status bar VA01 | trn03 | OVR; clock 14:05.

## 23. [13:38-13:38] Create Standard Order: Header Data (gui T-code=VA01)
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Create Standard Order: Header Data
- Orders
- Standard Order
- Purchase order no.
- dddd
- Sold-to party
- 1000
- Becker Berlin
- Calvinstrasse 36
- 13467 Berlin-Hermsdorf
- Sales
- Shipping
- Billing Document
- _(notes)_ Header Data screen with the 'Partners' tab page active, listing one row per partner function (AG/KB/RE/RG/VE/WE) with address data. Status bar VA01 | trn03 | OVR; clock 14:05.

## 24. [14:27-14:27] Create Standard Order: Overview (gui T-code=VA01)
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Create Standard Order: Overview
- Orders
- Standard Order
- Net value
- 0.00 EUR
- Sold-to party
- 1000
- Becker Berlin
- Calvinstrasse 36
- 13467 Berlin-Hermsdorf
- Ship-to party
- 1000
- PO Number
- _(notes)_ Back on the overview screen after the header/partner part; unchanged empty order. Status bar VA01 | trn03 | OVR; clock 14:06.

## 25. [14:29-14:29] Business Partners from the Customer Master <-> Create Standard Order: Overview (transition) (other T-code=VA01)
- Business Partners from the Customer Master
- Sold-to party
- Ship-to party
- Bill-to party
- Payer
- Customer master
- Create Standard Order: Overview
- Sales document  Edit  Goto  Extras  Environment  System  Help
- SAP Support Portal - Search for SAP Notes - Windows In...
- _(notes)_ Cross-fade frame between a slide and the live SAP GUI (both layers partly visible); not a clean slide or clean GUI screen. The partners slide is visible with the SAP GUI window fading in over it; cloc

## 26. [14:30-14:30] Business Partners from the Customer Master (slide)
- Business Partners from the Customer Master
- Sold-to party
- Ship-to party
- Bill-to party
- Payer
- Customer master
- _(notes)_ The partners slide shown clearly and centred (four party roles arranged around the Customer master oval); clock 14:06.

## 27. [14:42-14:42] Proposing Order Data from the Customer Master (slide)
- Proposing Order Data from the Customer Master
- Customer master
- C1
- Pricing
- Incoterms
- Shipping conditions
- Customer master
- R1
- Payment terms
- Credit limit check
- Customer master
- S1
- Delivery address
- Goods Receiving Hours
- _(notes)_ Slide mapping each order partner role to the customer master that proposes its data: C1 pricing/incoterms/shipping conditions, R1 payment terms/credit limit check, S1 delivery address/GR hours/tax, E1

## 28. [16:45-16:45] Business Data (slide)
- Business Data
- Order 1
- HEADER
- Payment cond. :  ZB01
- Incoterms :  FOB
- Item 10
- Payment cond.: ZB01
- Incoterms:  FOB
- Item 20
- Payment cond.: ZB01
- Incoterms:  FOB
- Copy
- Order 2
- HEADER
- _(notes)_ Slide with two orders copied from one another: header and item 10 keep ZB01/FOB, but in order 2 item 20 the payment condition (ZB01 ZB02) and incoterms (FOB EXW) differ and are struck through in red; 

## 29. [18:13-18:13] Create Standard Order: Overview with 'Business Data' slide overlaid (transition) (other T-code=VA01)
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Create Standard Order: Overview
- Orders
- Business Data
- HEADER
- Payment cond. : ZB01
- FOB
- at item level
- Standard Order
- Net value
- 0.00 EUR
- Sold-to party
- 1000
- Becker Berlin
- _(notes)_ Cross-fade frame between a slide and the live SAP GUI (both layers partly visible); not a clean slide or clean GUI screen. The overview screen is legible underneath while the incoming 'Business Data' 

## 30. [18:15-18:15] Create Standard Order: Overview (gui T-code=VA01)
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Create Standard Order: Overview
- Orders
- Standard Order
- Net value
- 0.00 EUR
- Sold-to party
- 1000
- Becker Berlin
- Calvinstrasse 36
- 13467 Berlin-Hermsdorf
- Ship-to party
- 1000
- PO Number
- _(notes)_ Same overview screen, now with the payment-terms entry ZB1 highlighted (blue selection) as the narrator points at header-level versus item-level payment conditions. Status bar VA01 | trn03 | OVR; cloc

## 31. [18:39-18:40] Create Standard Order: Item Data (gui T-code=VA01)
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Create Standard Order: Item Data
- Orders
- Sales Document
- Item
- 10
- Item category
- TAN
- Standard Item
- Material
- T-ATA30
- Screen 1
- Sales A
- Sales B
- _(notes)_ Item Data screen (Item 10, item category TAN, material T-ATA30) with the 'Order Quantity and Delivery Date' block: 10 PC, first delivery date 09.06.2007; 'All items' grid row 10 = T-ATA30 / 10 PC / Sc

## 32. [19:27-19:27] Create Standard Order: Overview (gui T-code=VA01)
- Create Standard Order: Overview
- Menu: Sales document | Edit | Goto | Extras | Environment | System | Help
- Toolbar button: Orders
- Standard Order (empty)   Net value 22,990.00 EUR
- Sold-to party 1000  Becker Berlin / Calvinstrasse 36 / 13467 Berlin-Hermsdorf
- Ship-to party 1000  Becker Berlin / Calvinstrasse 36 / 13467 Berlin-Hermsdorf
- PO Number dddd
- PO date (empty)
- Tabs: Sales | Item overview | Item detail | Ordering party | Procurement | Shipping | Reason for rejection
- Req. deliv.date D 09.06.2007
- Deliver.Plant (empty)
- Complete deliv. (checkbox, unchecked)
- Total Weight 205 KG
- Delivery block (empty)
- _(notes)_ SAP R/3 GUI demo screen, transaction VA01 (status bar VA01/trn03/OVR). Header data completed, one item T-ATA30 with qty 10 PC and plant 1200.

## 33. [19:30-19:32] Business Data (slide T-code=VA01)
- Business Data
- Order 1
- HEADER  Payment cond. : ZB01  |  Incoterms : FOB
- Copy (vertical arrow from HEADER down to the items)
- Order 2
- HEADER  Payment cond. : (value hidden behind the open dropdown list)
- Item 10 (box only partly drawn - mid animation)
- Open browser task list: 'SAP Support Portal - Search for SAP Notes - Windows In...', 'SAP Education - Windows Internet Explorer', 'SAP Education - Windows Internet Explorer'
- Status bar of the ghosted GUI behind: VA01  trn03  OVR
- Taskbar clock 14:11
- Item 10  Payment cond. : ZB01  |  Incoterms : FOB
- Item 20  Payment cond. : ZB01  |  Incoterms : FOB
- Copy (arrow from Order 1 HEADER to Item 10, Copy arrow from Order 1 HEADER to Item 20)
- Item 20  Payment cond. : ZB01 ZB02  |  Incoterms : FOB EXW   (ZB01 and FOB struck through, ZB02 and EXW added)
- _(notes)_ IE window 'SAP Education - Windows Internet Explorer' showing a PowerPoint slide mid-build; the previously shown VA01 screen still ghosts through and the browser's open-window list covers part of the 

## 34. [19:51-19:52] Proposing Plants Automatically (slide)
- Proposing Plants Automatically
- Customer material info:
- C1  M1  Cust.mat.  PC-100
- Delivering plant: 1400
- Customer master S1
- Delivering plant: 1100
- Material master M1   (greyed out / not yet faded in)
- Sold-to party : K1
- Ship-to party : S1
- Item | Customer material | Quantity | Plant
- 10 | PC-100 | 10 | 1400
- Sold-to party : K2
- Ship-to party : S1
- Item | Material | Quantity | Plant
- _(notes)_ Slide captured mid-animation: the Material master M1 cylinder and the C3 order row are still greyed out; only the first two orders are fully readable.

## 35. [21:36-21:37] Lesson Summary (slide)
- Lesson Summary
- You should now be able to:
- Determine the origin of document data from various sources, like the material master, the customer master, or Customizing
- (ghosted text from the previous slide fading out: Customer material info:, C1 M1 Cust.mat. PC-100, Delivering plant: 1400, Customer master S1, Delivering plant: 1100, Material master M1, Delivering plant: 1000, Material master M2, Delivering plant: 1200, Sold-to party : K1/Ship-to party : S1, Item | Customer material | Quantity | Plant, 10 PC-100 10 1400, Sold-to party : K2/Ship-to party : S1, 10 M1 10 1100, 20 M2 10 1100, Sold-to party : C3/Ship-to party : S2, 10 M1 10 1000, 20 M2 10 1200)
- Taskbar clock 14:13
- (previous slide now almost fully faded, only faint outlines remain)
- _(notes)_ Cross-fade transition frame: the 'Proposing Plants Automatically' slide is still clearly visible behind the Lesson Summary text.

## 36. [21:53-21:53] Proposing Plants Automatically (slide)
- Proposing Plants Automatically
- Customer material info:
- C1   M1   Cust.mat.   PC-100
- Delivering plant: 1400
- Customer master S1
- Delivering plant: 1100
- Material master M1
- Delivering plant: 1000
- Material master M2
- Delivering plant: 1200
- Sold-to party : K1
- Ship-to party : S1
- Item | Customer material | Quantity | Plant
- 10 |  PC-100 | 10 | 1400
- _(notes)_ Slide shown again in full quality during the recap of the lesson (plant proposal logic).

## 37. [22:19-22:19] Lesson Summary (slide)
- Lesson Summary
- You should now be able to:
- Determine the origin of document data from various sources, like the material master, the customer master, or Customizing
- Tooltip over the navigation button: Next Page
- (a faint ghost of the 'Proposing Plants Automatically' slide is still visible)
- Taskbar clock 14:14
- _(notes)_ End-of-lesson summary slide; the pointer rests on the course player's forward button, whose tooltip 'Next Page' is displayed.

## 38. [22:45-22:45] Sales Summary (slide)
- Sales Summary
- Sales Summary for Customer 5264
- Address
- FA IDES
- Neurottstr. 16
- D-69190 Walldorf
- Key figures
- Annual sales 200 000 000 UNI
- Employees 604
- Legal status Limited liability company
- Quick info
- Last order 5638
- Max. credit limit used 68 %
- Orders blocked for billing 2
- _(notes)_ Concept slide that introduces the Sales Summary info blocks shown later in the VA01 demo; sample customer 5264 (FA IDES, Walldorf).

## 39. [23:23-23:24] Create Standard Order: Overview (gui T-code=VA01)
- Create Standard Order: Overview
- Menu: Sales document | Edit | Goto | Extras | Environment | System | Help
- Toolbar button: Orders
- Standard Order (empty)   Net value 22,990.00 EUR
- Sold-to party 1000  Becker Berlin / Calvinstrasse 36 / 13467 Berlin-Hermsdorf
- Ship-to party 1000  Becker Berlin / Calvinstrasse 36 / 13467 Berlin-Hermsdorf
- PO Number dddd
- PO date (empty)
- Tabs: Sales | Item overview | Item detail | Orderi... (Ordering party)
- Req. deliv.date D 09.06.2007
- Complete deliv. (checkbox, unchecked)
- Delivery block (empty)
- Billing block (empty)
- Payment card (empty)
- _(notes)_ Capture is a cross-fade: the VA01 order screen is only semi-drawn, so the previous 'Sales Summary' slide shows through and some tab/field text is cut off. Same screen as t01167/t01404.

## 40. [24:09-25:18] Sales Summary (gui T-code=VA01)
- Sales Summary
- Menu: Sales summary | Edit | Goto | Environment | System | Help
- Buttons: Info block | View
- Sales Summary for Customer 0000001000 Becker Berlin
- Address
- Firma
- Becker Berlin
- Calvinstraße 36
- D-13467 BERLIN-HERMSDORF
- Classification
- Nielsen ID
- Regional market
- Customer classif. Btw. 5,0 - 7,0 mill.
- Industry sector Manufacturing
- _(notes)_ Sales Summary overview screen called from the order (VA01/trn03/OVR in the status bar). Contact person table is still empty in this frame.

## 41. [25:24-25:24] Delivery 80007832 Display: Overview (gui T-code=VA01)
- Delivery 80007832 Display: Overview
- Menu: Outbound Delivery | Edit | Goto | Extras | Environment | Subsequent Functions | System | Help
- Button: Post goods issue (greyed out)
- Outbound deliv. 80007832
- Document Date 22.11.2000
- Ship-to party 1000  Becker Berlin / Calvinstrasse 36 / 13467 Berlin-Hermsdorf
- Tabs: Item Overview | Picking | Loading | Transport | Status Overview | Goods Movement Data
- Planned GI 21.11.2000 00:00
- Actual GI date 23.11.2000
- Plnd gds mvt: Net Val 0.00 EUR
- All items
- Item | Material | Delivery quantity | SU | Description | B. | ItCa | P | WBatch | Val. type | Open quantity
- 10 | P-102 | 26 PC | Pumpe PRECISION 102 | | TAN | C | C | | 26
- 20 | P-104 | 39 PC | Pumpe PRECISION 104 | | TAN | C | C | | 39
- _(notes)_ Outbound delivery display opened from the Sales Summary quick-info link 'Last delivery 80007832'; the SAP status bar still reports VA01/trn03/OVR, and the underlying Sales Summary rows ghost through a

## 42. [25:25-25:54] Sales Summary (gui T-code=VA01)
- Sales Summary
- Menu: Sales summary | Edit | Goto | Environment | System | Help
- Buttons: Info block | View
- Sales Summary for Customer 0000001000 Becker Berlin
- Credit Limit 511,291.88 EUR
- Usage Level 1,472,653.29 EUR
- Delta 961,361.41- EUR
- Consumption in % 288
- Payment history
- Receivables 835,166.13 EUR
- Special Liabilities 0.00 EUR
- Open Delivery Value 528,437.42 EUR
- Open Sales Order Val 109,049.74 EUR
- Open Bill. Doc. Val 0.00 EUR
- _(notes)_ Same Sales Summary view one second later, back from the delivery display; the highlighting on the 'Last delivery' line is gone.

## 43. [25:55-25:55] Customizing: Execute Project (gui T-code=SPRO)
- Customizing: Execute Project
- Menu: Project | Edit | Goto | Settings | Tools | System | Help
- Tabs: SAP Reference IMG | IMG Information | Project Analysis
- My Customizing Worklist
- Project | Name
- Button: Manage Worklist
- Status bar: SPRO  trn03  OVR
- Taskbar clock 14:18
- _(notes)_ Customizing (SPRO) 'Execute Project' screen with an empty 'My Customizing Worklist'; ends the demonstration of where document data can originate (master data and Customizing).

## 44. [26:03-26:45] Display IMG (gui T-code=SPRO)
- Implementation Guide  Edit  Goto  Additional Information  Utilities(M)  System  Help
- Display IMG
- Existing BC Sets | BC Sets for Activity | Activated BC Sets for Activity | Release Notes | Change Log | Where Else Used
- Structure
- SAP Customizing Implementation Guide
- Sales and Distribution (selected / highlighted)
- SPRO | tnn03 | OVR
- Activation Switch for SAP R/3 Enterprise Extension Set
- SAP NetWeaver
- Enterprise Structure
- Cross-Application Components
- Auto-ID Infrastructure
- Financial Accounting
- Financial Supply Chain Management
- _(notes)_ SAP R/3 GUI. Customizing (IMG) entry screen; whole tree collapsed, only 'Sales and Distribution' highlighted. Windows taskbar visible (开始 / 控制面板 / SAP Logon), clock 14:18.

## 45. [27:06-27:10] Change View "Maintain Report Views": Overview (gui T-code=SPRO)
- Table View  Edit  Goto  Selection  Utilities(M)  System  Help
- Change View "Maintain Report Views": Overview
- New Entries
- Position...
- | Info view | Description | Standard | Form |
- 001 | Complete information | (checked) | SD-SALES-SUMMARY
- 002 | Address/partner info | (empty) | SD-SALES-SUMMARY
- 003 | Statistical info | (empty) | SD-SALES-SUMMARY
- 005 | Telesales | (empty) | SD-SALES-SUMMARY
- 100 | Credit Information | (empty) | SD-SALES-SUMMARY
- 101 | Last SD Documents | (empty) | SD-SALES-SUMMARY
- 102 | Backorders | (empty) | SD-SALES-SUMMARY
- 103 | Quick Info | (empty) | SD-SALES-SUMMARY
- 900 | New Internet cust. | (empty) | SD-SALES-SUMMARY
- _(notes)_ Table-maintenance (SM30-style) overview for the reporting/Sales Summary views. Clock 14:19. Defines which views exist for the report evaluation.

## 46. [27:11-27:11] Display IMG (gui T-code=SPRO)
- Implementation Guide  Edit  Goto  Additional Information  Utilities(M)  System  Help
- Display IMG
- Existing BC Sets | BC Sets for Activity | Activated BC Sets for Activity | Release Notes | Change Log | Where Else Used
- Maintain Copy Control for Sales Documents
- Maintain Display of Date Category and Periods
- Lists
- Set Updating Of Partner Index
- Set Updating Of Item Index
- Define Selection Criteria
- Define List Layout Of Expected Customer Price
- Sales Returns
- Part Load Lift Orders
- Foreign Trade/Customs
- Billing
- _(notes)_ Back to the IMG navigation view with Sales Summary expanded, showing the four report-view customizing activities. Clock 14:19.

## 47. [27:16-27:16] Change View "Maintain Views for an Evaluation": Overview (gui T-code=SPRO)
- Table View  Edit  Goto  Selection  Utilities(M)  System  Help
- Change View "Maintain Views for an Evaluation": Overview
- New Entries
- Position...
- | Info view | Description | Sequence | Description |
- 001 | Complete information | 001 | Address
- 001 | Complete information | 002 | Customer Classific.
- 001 | Complete information | 003 | Performance Measures
- 001 | Complete information | 004 | Contact persons
- 001 | Complete information | 005 | Sales Order Info
- 001 | Complete information | 006 | Customer Pricing
- 001 | Complete information | 007 | Cust Delivery Info
- 001 | Complete information | 008 | Partial Deliv. Info
- 001 | Complete information | 009 | Cust Transport Info
- _(notes)_ The 'Assign Information Blocks To A View' table: 51 information blocks assigned to view 001 in sequence. Clock 14:19.

## 48. [27:27-27:27] Change View "Maintain Views for an Evaluation": Details (gui T-code=SPRO)
- Table View  Edit  Goto  Selection  Utilities(M)  System  Help
- Change View "Maintain Views for an Evaluation": Details
- Info view        001  Complete information
- Sequence        001
- Info block        1  Address
- Form Info
- Window          MAIN
- Element         LIST1_001
- SPRO | tnn03 | OVR
- _(notes)_ Detail screen reached by double-clicking row 001/001 of the previous overview: shows how the info block 'Address' is mapped to a form window/element. Clock 14:19.

## 49. [27:33-27:33] Display IMG (with "Maintain Views for an Evaluation" table window behind) (gui T-code=SPRO)
- Implementation Guide  Edit  Goto  Additional Information  Utilities(M)  System  Help
- Display IMG
- Existing BC Sets | BC Sets for Activity | Activated BC Sets for Activity | Release Notes | Change Log | Where Else Used
- Maintain Copy Control for Sales Documents
- Maintain Display of Date Category and Periods
- Lists
- Set Updating Of Partner Index
- Set Updating Of Item Index
- Define Selection Criteria
- Define List Layout Of Expected Customer Price
- Sales Returns
- Part Load Lift Orders
- Foreign Trade/Customs
- Billing
- _(notes)_ Transition frame: IMG tree window is on top and the previous table view (rows 013-017, Entry 1 of 51) is visible underneath - narrator returning from the table to the IMG tree. Clock 14:19.

## 50. [27:34-27:34] Display IMG (gui T-code=SPRO)
- Implementation Guide  Edit  Goto  Additional Information  Utilities(M)  System  Help
- Display IMG
- Existing BC Sets | BC Sets for Activity | Activated BC Sets for Activity | Release Notes | Change Log | Where Else Used
- Lists
- Set Updating Of Partner Index
- Set Updating Of Item Index
- Define Selection Criteria
- Define List Layout Of Expected Customer Price
- Sales Returns
- Part Load Lift Orders
- Foreign Trade/Customs
- Billing
- Sales Support (CAS)
- Sales Activities
- _(notes)_ IMG tree scrolled further down; the four Sales Summary activities are visible together with the nodes below Sales and Distribution. Clock 14:19.

## 51. [27:48-27:48] Change View "Maintain the Report Views for a User": Overview (gui T-code=SPRO)
- Table View  Edit  Goto  Selection  Utilities(M)  System  Help
- Change View "Maintain the Report Views for a User": Overview
- New Entries
- Position...
- | User | Info view | Description |
- BAPMS | ZPD | Precision Drilling V
- WF-SD-2 | 900 | New Internet cust.
- Entry 1 of 2
- SPRO | tnn03 | OVR
- _(notes)_ The 'Assign Default View To User' table: two user/view assignments. Clock 14:20.

## 52. [27:56-27:56] Display IMG (gui T-code=SPRO)
- Implementation Guide  Edit  Goto  Additional Information  Utilities(M)  System  Help
- Display IMG
- Existing BC Sets | BC Sets for Activity | Activated BC Sets for Activity | Release Notes | Change Log | Where Else Used
- Lists
- Set Updating Of Partner Index
- Set Updating Of Item Index
- Define Selection Criteria
- Define List Layout Of Expected Customer Price
- Sales Returns
- Part Load Lift Orders
- Foreign Trade/Customs
- Billing
- Sales Support (CAS)
- Sales Activities
- _(notes)_ Identical screen position to t01654 (same IMG scroll offset); clock advanced to 14:20 - narrator back on the IMG activity list after the table maintenance.

## 53. [27:59-27:59] Display IMG (table dialog "Statistics update desired" overlapping) (gui T-code=SPRO)
- Table View  Edit  Goto  Selection  Utilities(M)  System  Help
- Display IMG
- New Entries
- | Document cat. | Description | Statistics update desired |
- 1 | Sales activities (CAS) | (unchecked)
- 2 | External transaction | (unchecked)
- 3 | Invoice list | (unchecked)
- 4 | Credit memo list | (unchecked)
- 5 | Intercompany invoice | (unchecked)
- 6 | Intercompany credit me | (unchecked)
- A | Inquiry | (unchecked)
- B | Quotation | (checked)
- C | Order | (checked)
- D | Item proposal | (unchecked)
- _(notes)_ A table-maintenance dialog overlays the IMG tree (same header row as the 'Last Documents for a Customer' table: Document cat. / Description / Statistics update desired). Clock 14:20.

## 54. [28:00-28:00] Change View "Last Documents for a Customer": Overview (gui T-code=SPRO)
- Table View  Edit  Goto  Selection  Utilities(M)  System  Help
- Change View "Last Documents for a Customer": Overview
- New Entries
- Position...
- | Document cat. | Description | Statistics update desired |
- 1 | Sales activities (CAS) | (unchecked)
- 2 | External transaction | (unchecked)
- 3 | Invoice list | (unchecked)
- 4 | Credit memo list | (unchecked)
- 5 | Intercompany invoice | (unchecked)
- 6 | Intercompany credit me | (unchecked)
- A | Inquiry | (unchecked)
- B | Quotation | (checked)
- C | Order | (checked)
- _(notes)_ Full-screen overview of the same customizing table named in the title: which sales document categories appear in the 'Last Documents for a Customer' info block. 30 entries total. Clock 14:20.

## 55. [28:27-28:27] Change View "Last Documents for a Customer": Overview (IMG structure pane, scrolled) (gui T-code=SPRO)
- Implementation Guide  Edit  Goto  Additional Information  Utilities(M)  System  Help
- Change View "Last Documents for a Customer": Overview
- Structure
- Lists
- Set Updating Of Partner Index
- Set Updating Of Item Index
- Define Selection Criteria
- Define List Layout Of Expected Customer Price
- Sales Returns
- Part Load Lift Orders
- Foreign Trade/Customs
- Billing
- Sales Support (CAS)
- Sales Activities
- _(notes)_ Same table transaction as t01680 but showing the left-hand IMG structure pane (activity list) instead of the data grid. Clock 14:20.

## 56. [28:29-28:29] Display IMG (gui T-code=SPRO)
- Implementation Guide  Edit  Goto  Additional Information  Utilities(M)  System  Help
- Display IMG
- Existing BC Sets | BC Sets for Activity | Activated BC Sets for Activity | Release Notes | Change Log | Where Else Used
- Maintain Display of Date Category and Periods
- Lists
- Set Updating Of Partner Index
- Set Updating Of Item Index
- Define Selection Criteria
- Define List Layout Of Expected Customer Price
- Sales Returns
- Part Load Lift Orders
- Foreign Trade/Customs  (highlighted band)
- Billing
- Sales Support (CAS)
- _(notes)_ Final frame of the chunk: IMG tree scrolled with 'Lists' expanded and the Sales Summary activities visible; duplicate 'Lists' rows and highlight bands are repaint/encoding artifacts. Clock 14:20.

## 57. [28:51-28:51] Sales Summary (for Customer 0000001000 Becker Berlin) (gui T-code=VA01)
- Sales summary  Edit  Goto  Environment  System  Help
- Sales Summary
- Info block
- View
- Sales Summary for Customer 0000001000 Becker Berlin
- Usage Level        1,472,653.29 EUR
- Delta             -961,361.41- EUR
- Consumption in %   288
- Payment history
- Special Liabilities      0.00 EUR
- Open Delivery Value     528,437.42 EUR
- Open Sales Order Val    109,049.74 EUR
- Open Bill. Doc. Val       0.00 EUR
- Quick info
- _(notes)_ SAP GUI live demo. Sales Summary screen reached from the sales-order environment (menu bar 'Sales summary'), status bar shows transaction VA01. Windows taskbar is Chinese-localised (开始 / 控制面板), time 1

## 58. [28:58-28:58] Sales Summary (sales-order view, tab strip on screen) (gui T-code=VA01)
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Sales Summary
- Orders
- Standard Order          Net value      22,990.00 EUR
- Sold-to party   1000   Becker Berlin / Calvinstrasse 36 / 13467 Berlin-Hermsdorf
- Ship-to party   1000
- PO Number        288
- Open Sales Order Val              109,049.74 EUR
- Open Bill. Doc. Val                    0.00 EUR
- Sales   Item overview   Item detail   Ordering party   Procurement   Shipping   Reason for rejection
- Req. delv.date   D   09.06.2007
- Complete delv.
- Delivery block
- Billing block
- _(notes)_ SAP GUI live demo. Screen is the Sales Summary displayed from within the sales order (menu bar 'Sales document' plus the order tab strip), status bar VA01. A Ship-to-party search/autocomplete popup is

## 59. [28:59-28:59] Create Standard Order: Overview (gui T-code=VA01)
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Create Standard Order: Overview
- Standard Order          Net value      22,990.00 EUR
- Sold-to party   1000   Becker Berlin / Calvinstrasse 36 / 13467 Berlin-Hermsdorf
- Ship-to party   1000
- PO Number      ddddd
- PO date
- Open Sales Order Val              109,049.74 EUR
- Open Bill. Doc. Val                    0.00 EUR
- Sales   Item overview   Item detail   Ordering party   Procurement   Shipping   Reason for rejection
- Req. delv.date   D   09.06.2007
- Complete delv.
- Delivery block
- Billing block
- _(notes)_ SAP GUI live demo, tcode VA01. Same screen as t01738 after the Ship-to-party selection was completed; the first order line item (material T-ATA30, qty 10 PC TAN) has been entered, further item rows ar

## 60. [29:15-29:15] Create Sales.Order: Initial Screen (gui T-code=VA01)
- Sales document   Edit   Goto   Environment   System   Help
- Create Sales.Order: Initial Screen
- Create with Reference
- Sales
- Item overview
- Ordering party
- Order Type       OR      Standard Order
- Organizational data
- Sales Organization
- Distribution Channel
- Division
- Sales Office
- Sales Group
- _(notes)_ SAP GUI live demo, tcode VA01 (status bar). Initial creation screen with the order type OR / Standard Order selected and the organizational-data group empty. Taskbar icons and command field visible; c

## 61. [29:25-29:25] Create Sales.Order: Initial Screen (with SAP menu tree expanded) (gui T-code=VA01)
- Sales document   Edit   Goto   Environment   System   Help
- Create Sales.Order: Initial Screen
- Other menu
- Create role
- Favorites
- SAP menu
- Office
- Cross-Application Components
- Auto-ID Infrastructure
- Collaboration Projects
- Logistics
- Materials Management
- Sales and Distribution
- Master Data
- _(notes)_ SAP GUI live demo, tcode VA01. Same initial screen as t01755 but the SAP Easy Access navigation area (Favorites / SAP menu tree) is docked and expanded, showing the Sales and Distribution branch. Stat

## 62. [29:28-29:33] SAP Easy Access (gui T-code=SESSION_MANAGER)
- SAP Easy Access
- Menu   Edit   Favorites   Extras   System   Help
- Other menu
- Create role
- Assign users
- Documentation
- Favorites
- SAP menu
- Office
- Cross-Application Components
- Logistics
- Materials Management
- Sales and Distribution
- Master Data
- _(notes)_ SAP GUI live demo, status bar shows SESSION_MANAGER (SAP Easy Access happens to be the current screen). Right-hand pane shows the SAP water-ripple logo graphic. Clock 14:21.

## 63. [29:48-29:48] Sales Summary (initial selection screen) (gui T-code=VC/2)
- Program   Edit   Goto   System   Help
- Sales Summary
- Customer
- Customer number   1000        to
- Dynamic selections
- Sales area
- Sales organization   1000
- Distribution channel
- Division
- _(notes)_ SAP GUI live demo of transaction VC/2 (Sales Summary) selection screen, entered with a fresh session; status bar VC/2. SAP splash logo top-right. Clock 14:22.

## 64. [30:12-30:12] Sales Summary for Customer 0000001000 Becker Berlin (gui T-code=VC/2)
- Program   Edit   Goto   System   Help
- Sales Summary
- Info block
- View
- Address
- Firma
- Becker Berlin
- Calvinstrasse 36
- D-13467 BERLIN-HERMSDORF
- Classification
- Nielsen ID                 Regional market
- Customer classif.          Btw. 5,0 - 7,0 mill.
- Industry sector            Manufacturing
- Key figures
- _(notes)_ SAP GUI result screen of transaction VC/2 for sold-to party 1000; 'Key figures' block is empty for this customer. Clock 14:22.

## 65. [30:26-30:26] Sales Summary (initial selection screen) (gui T-code=VC/2)
- Program   Edit   Goto   System   Help
- Sales Summary
- Customer
- Customer number   1000        to
- Dynamic selections
- Sales area
- Sales organization   1000
- Distribution channel
- Division
- _(notes)_ SAP GUI, transaction VC/2 selection screen again; a SAP water-ripple splash artifact is overlaid mid-screen. Clock 14:22.

## 66. [30:28-30:33] Sales Summary (with SAP Easy Access navigation area) (gui T-code=VC/2)
- Menu   Edit   Favorites   Extras   System   Help
- Other menu
- Create role
- Assign users
- Documentation
- Sales Summary
- Customer
- Customer number   1000        to
- Dynamic selections
- Sales area
- Sales organization   1000
- Distribution channel
- Division
- _(notes)_ SAP GUI. The SAP Easy Access menu bar and its toolbar row (Other menu / Create role / Assign users / Documentation) are displayed together with the VC/2 Sales Summary selection screen; SAP logo graphi

## 67. [30:37-30:37] Sales Summary (SAP Education help page in Windows Internet Explorer) (other)
- Sales Summary
- Sales Summary for Customer 5264
- Sales area
- Sales organization   1000
- Distribution channel
- Division
- Info blocks
- Address
- Key figures
- Quick info
- Contact person
- Last SD documents
- Document key figures
- Pricing
- _(notes)_ Not a slide and not the SAP GUI: an Internet Explorer window titled 'SAP Education' displaying the SAP online help/documentation page for the Sales Summary. The illustration caption reads 'Sales Summa

## 68. [30:50-30:50] Sales Summary (SAP Education help page, populated example) (other)
- Sales Summary
- Sales Summary for Customer 5264
- Sales area
- Sales organization   1000
- Distribution channel
- Division
- Info blocks
- Address
- Key figures
- Quick info
- Contact person
- Last SD documents
- Document key figures
- Pricing
- _(notes)_ Same SAP Education help page as t01837, now showing the complete example. A Windows taskbar jump-list is open (Display IMG, SAP Easy Access, SAP Logon 710). Clock 14:23.

## 69. [30:52-30:53] SAP Easy Access (over the open help page) (gui)
- Menu   Edit   Favorites   Extras   System   Help
- Other menu
- Create role
- Sales Summary
- Sales Summary for Customer 5264
- Assign users
- Documentation
- Sales Summary for Custo
- Address
- FA IDES
- Neurottstr. 16
- D-69190 Walldorf
- Key figures
- Annual sales        200 000 000 UNI
- _(notes)_ SAP GUI window (SAP Easy Access menu bar and toolbar) brought to the foreground over the IE help page; a large SAP water-ripple splash graphic covers part of the window, so the SAP status bar text is 

## 70. [30:55-30:55] Sales Summary (initial selection screen, new session) (gui T-code=VC/2)
- Program   Edit   Goto   System   Help
- Sales Summary
- Customer
- Customer number   1000        to
- Dynamic selections
- Sales area
- Sales organization   1000
- Distribution channel
- Division
- _(notes)_ SAP GUI, transaction VC/2 selection screen in a fresh GUI window; SAP watermark artifacts and a taskbar jump-list (SAP Easy Access, SAP Logon 710) are visible. Status bar VC/2 trn03 OVR. Clock 14:23.

## 71. [30:56-30:56] Sales Summary (initial selection screen) (gui T-code=VC/2)
- Program   Edit   Goto   System   Help
- Sales Summary
- Customer
- Customer number   1000        to
- Dynamic selections
- Sales area
- Sales organization   1000
- Distribution channel
- Division
- _(notes)_ SAP GUI VC/2 selection screen, clean render of the same content as t01855 (no splash artifacts). Status bar VC/2 trn03 OVR. Clock 14:23.

## 72. [31:05-31:05] Sales Summary (with customer-master input help popup) (gui T-code=VC/2)
- Program   Edit   Goto   System   Help
- Sales Summary
- General Data in Customer Master
- Customer Master Contact Partner
- Customer Master Partner Functions
- Customer Master Sales Data
- Customer
- Customer number   1000        to
- Dynamic selections
- Sales area
- Sales organization   1000
- Distribution channel
- Division
- _(notes)_ SAP GUI. The F4 possible-entries (input help) list for the customer field is expanded, listing the customer-master matchcode views; the menu bar is greyed out while the popup is open. Status bar VC/2 

## 73. [31:15-31:29] Sales Summary (gui T-code=VC/2)
- Program   Edit   Goto   System   Help
- Sales Summary
- Customer
- Customer number              1000    to
- Dynamic selections
- Sales area
- Sales organization           1000
- Distribution channel
- Division
- Use
- ...les:
- _(notes)_ Live SAP GUI initial (selection) screen of the customer Sales Summary. Status bar bottom-right reads 'VC/2 | trn03 | OVR' (left field is the transaction code VC/2; middle field 'trn03' appears constan

## 74. [31:38-31:38] Sales Summary - Customer 0000001000 Becker (gui T-code=VC/2)
- Sales summary   Edit   Goto   Environment   System   Help
- Sales Summary
- Address
- Firma
- Becker Berlin
- Calvinstrasse 36
- D-13467 BERLIN-HERMSDORF
- Classification
- Nielsen ID                = Regional market
- Customer classif.         = Btw. 5,0 - 7,0 mill.
- Industry sector           = Manufacturing
- _(notes)_ Result screen of the Sales Summary for customer 1000 (Becker). Toolbar shows the buttons 'Info block' and 'View'; menu bar switched from 'Program' to 'Sales summary'. Status bar 'VC/2 | trn03 | OVR'.

## 75. [31:50-31:50] Sales Summary - Info View Selection (gui T-code=VC/2)
- Sales summary   Edit   Goto   Environment   System   Help
- Sales Summary
- Info View Selection
- ID
- View
- 001   Complete information
- 002   Address/partner info
- 003   Statistical info
- 005   Telesales
- 100   Credit Information
- 101   Last SD Documents
- 102   Backorders
- 103   Quick Info
- 900   New Internet cust.
- _(notes)_ The 'Info View Selection' dialog (confirm ✓ / cancel ✗ buttons) is opened over the Sales Summary; the instructor picks which info views to display. Behind it the Address, Classification, Key figures a

## 76. [31:53-31:53] Sales Summary - Last SD documents (gui T-code=VC/2)
- Sales summary   Edit   Goto   Environment   System   Help
- Sales Summary
- Last SD documents
- Order        Date          Net Value        Status
- 11076        13.05.07        100.00 EUR     Open
- 11075        13.05.07        100.00 EUR     Open
- 11074        13.05.07        100.00 EUR     Open
- 11072        16.03.06     52,000.00 EUR     Open
- 10765        21.01.05    300,000.00 EUR     Open
- Invoice      Date          Net Value        Status
- 90035240     21.01.05     30,000.00 EUR     Completed
- 90033630     08.04.03     24,000.00 EUR     Being processed
- 90033619     28.03.03     60,000.00 EUR     Being processed
- 90023097     24.11.00    536,088.60 EUR     Being processed
- _(notes)_ Scrolled-down view of the same Sales Summary showing the 'Last SD documents' block: open orders and invoice list with net values and status. Status bar 'VC/2 | trn03 | OVR'.

## 77. [32:07-32:07] Sales Summary - Statistical Information / Info View Selection (gui T-code=VC/2)
- Sales summary   Edit   Goto   Environment   System   Help
- Sales Summary
- Info View Selection
- 001   ...information
- 002   ...rther info
- 003   ...l info
- 005   Telesales
- 100   Credit Information
- 101   Last SD Documents
- 102   Backorders
- 103   Quick Info
- 900   New Internet cust.
- ZP2   Precision Drilling 2
- ZPD   Precision Drilling V
- _(notes)_ Statistical Information key figures and the Info View Selection dialog are shown simultaneously; a large black selection bar and the popup occlude most column values, so many row labels and all figure

## 78. [32:09-32:09] Sales Summary - Statistical Information 2007/2006 (gui T-code=VC/2)
- Sales summary   Edit   Goto   Environment   System   Help
- Sales Summary
- Statistical Information
- Net value of incoming orders
- Net sales
- Open net value of orders
- Net value of inc. returns
- Net value of credit memos
- Number of order items
- No.of returns items
- 2007        2006
- 300.00      52,000.00 EUR
- 0.00        0.00 EUR
- 300.00      52,000.00 EUR
- _(notes)_ Clear full view of the Statistical Information block (comparison of fiscal years 2007 vs 2006) together with the Last SD documents list. 'Info block' and 'View' toolbar buttons appear pressed. Status 

## 79. [32:28-32:28] Sales Summary (initial screen, redrawing) (gui T-code=VC/2)
- Program   Edit   Goto   System   Help
- Sales Summary
- Customer
- Customer number              1000    to
- Dynamic selections
- Sales area
- Sales organization           1000
- Distribution channel
- 300.00      52,000.00 EUR
- 0.00        0.00 EUR
- 300.00      52,000.00 EUR
- _(notes)_ The report has been exited / the screen is being repainted back to the initial selection screen: the menu bar is 'Program' again and stray Statistical Information figures (300.00, 52,000.00 EUR, 0.00)

## 80. [32:29-32:29] Sales Summary (initial screen, blocks cleared) (gui T-code=VC/2)
- Program   Edit   Goto   System   Help
- Sales Summary
- Customer
- Customer number              1000    to
- Sales area
- Sales organization           1000
- _(notes)_ Mid-redraw frame: the lower part of the screen is blank and only field outlines remain; no Statistical Information figures visible anymore. Status bar 'VC/2 | trn03 | OVR'.

## 81. [32:31-32:32] SAP Easy Access (gui T-code=VC/2)
- Menu   Edit   Favorites   Extras   System   Help
- SAP Easy Access
- Other menu
- Create role
- Assign users
- Documentation
- Favorites
- SAP menu
- Office
- Cross-Application Components
- Auto-ID Infrastructure
- Collaboration Projects
- Logistics
- Materials Management
- _(notes)_ The user has jumped back to the SAP Easy Access start screen; the menu tree is only partially painted (screen still refreshing) over the blue concentric-ripple background picture. The status bar still

## 82. [32:36-32:36] SAP Easy Access - Sales and Distribution > Sales Support > Information system (gui T-code=SESSION_MANAGER)
- Menu   Edit   Favorites   Extras   System   Help
- SAP Easy Access
- Other menu
- Create role
- Assign users
- Documentation
- Favorites
- SAP menu
- Office
- Cross-Application Components
- Auto-ID Infrastructure
- Collaboration Projects
- Logistics
- Materials Management
- _(notes)_ The navigation path to the Sales Summary is demonstrated in the standard menu: Sales and Distribution > Sales Support > Information system, where 'VC/2 - Sales Summary' is highlighted. On this screen 

## 83. [32:50-32:50] Sales Summary for Customer 5264 (slide)
- Sales Summary for Customer 5264
- Address
- FA IDES
- Neurottstr. 16
- D-69190 Walldorf
- Key figures
- Annual sales         200 000 000   UNI
- Employees                    604
- Legal status   Limited liability company
- Quick info
- Last order                                 5638
- Max. credit limit used                       68 %
- Orders blocked for billing                     2
- Info blocks
- _(notes)_ PowerPoint-style slide shown on top of the SAP window (client area still grey during redraw). Slide explains the structure of the Sales Summary screen: on the left a mock-up with Address / Key figures

## 84. [32:51-32:51] Overview: Changing of sales ... (slide)
- Overview: Changing of sales d...
- Sales Summary for Customer 5264
- Address
- FA IDES
- Neurottstr. 16
- D-69190 Walldorf
- Key figures
- Annual sales         200 000 000   UNI
- Employees                    604
- Legal status   Limited liability company
- Quick info
- Last order                                 5638
- Max. credit limit used                       68 %
- Orders blocked for billing                     2
- _(notes)_ The slide is now displayed inside a Windows Internet Explorer window titled 'SAP Education - Windows Internet Explorer'. The slide title is partly covered by a black screen-annotation marker ('Overvie

## 85. [32:52-32:52] Overview: Changing of sales documents (slide)
- Overview: Changing of sales documents
- Fast changes in document
- Order
- Item 10   Mat-12     Plant   1200   2000
- Item 20   Mat-10     Plant   1200   2000
- ...       ...        ...      ...    ...
- Concurrent change to several items
- Fast change of several documents
- Order
- ...ler      ...ler      ...ler
- Plant   1200   2000
- Plant   1200   2000
- Plant   1200   2000
- Plant   1200   2000
- _(notes)_ Full-width slide in Internet Explorer explaining two ways of mass-changing sales documents: (1) 'Fast changes in document' – change several items of one order at once in the item overview (plant 1200 

## 86. [33:51-33:53] SAP Easy Access (gui)
- Menu   Edit   Favorites   Extras   System   Help
- SAP Easy Access
- Other menu
- Create role
- Fast changes in document
- Order
- Item 10   Mat-12   Plant   1200   2000
- Item 20   Mat-10   Plant   1200   2000
- Concurrent change to several items
- Fast change of several documents
- Order
- Plant   1200   2000
- Changes using document list
- Display IMG
- _(notes)_ Back in the SAP GUI: the SAP Easy Access window is reopening and its client area has not been painted yet, so the desktop wallpaper (the previous 'Changing of sales documents' slide) shows through. A 

## 87. [33:54-33:54] SAP Easy Access - Sales and Distribution > Sales Support > Information system (gui T-code=SESSION_MANAGER)
- Menu   Edit   Favorites   Extras   System   Help
- SAP Easy Access
- Other menu
- Create role
- Assign users
- Documentation
- Favorites
- SAP menu
- Office
- Cross-Application Components
- Auto-ID Infrastructure
- Collaboration Projects
- Logistics
- Materials Management
- _(notes)_ Standard SAP menu path to the Sales Summary: Sales and Distribution > Sales Support > Information system, with 'VC/2 - Sales Summary' highlighted in the transaction list. Desktop wallpaper slide still

## 88. [33:55-33:55] SAP Easy Access (gui T-code=SESSION_MANAGER)
- Menu   Edit   Favorites   Extras   System   Help
- SAP Easy Access
- Other menu
- Create role
- Assign users
- Documentation
- Favorites
- SAP menu
- Office
- Cross-Application Components
- Auto-ID Infrastructure
- Collaboration Projects
- Logistics
- Materials Management
- _(notes)_ Paint-in frame of the same SAP Easy Access screen: the background picture (blue/white swirl) is being drawn over the desktop slide; the lower half of the client area is still grey. Status bar 'SESSION

## 89. [33:56-33:56] SAP Easy Access - Sales and Distribution > Sales Support > Information system (gui T-code=SESSION_MANAGER)
- Menu   Edit   Favorites   Extras   System   Help
- SAP Easy Access
- Other menu
- Create role
- Assign users
- Documentation
- Favorites
- SAP menu
- Office
- Cross-Application Components
- Auto-ID Infrastructure
- Collaboration Projects
- Logistics
- Materials Management
- _(notes)_ Fully painted SAP Easy Access screen with the blue/white swirl background picture, the expanded tree and 'VC/2 - Sales Summary' highlighted. Status bar 'SESSION_MANAGER | trn03 | OVR'. Clock 14:26.

## 90. [34:00-34:00] Create Sales Order: Initial Screen (gui T-code=VA01)
- Sales document   Edit   Goto   Environment   System   Help
- Create Sales Order: Initial Screen
- Create with Reference
- Sales
- Item overview
- Ordering party
- Order Type               OR      Standard Order
- Organizational data
- Sales Organization      1000     Germany Frankfurt
- Distribution Channel
- Division
- Sales Office
- Sales Group
- _(notes)_ The instructor switches to transaction VA01: 'Create Sales Order: Initial Screen'. The Order Type field contains 'OR' and the possible-entries list opened on it shows 'Standard Order'. The 'Organizati

## 91. [34:02-35:50] Create Standard Order: Overview (gui T-code=VA01)
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Create Standard Order: Overview
- Standard Order | Net value
- Sold-to party (input help open: t-s62130, t-s62100)
- Ship-to party
- PO Number
- Sales | Item overview | Item detail | Ordering party | Procurement | Shipping | Reason for rejection
- Req. deliv. date | Complete deliv. | Deliver.Plant
- Delivery block | Total Weight
- Billing block | Volume
- Payment card | Pricing date
- Payment terms | Exp.date
- Order reason | Incoterms
- Sales area  1000 / / Germany Frankfurt
- _(notes)_ Live SAP GUI. Sold-to party input help (F4) list open showing customer entries t-s62130 / t-s62100; item table still empty (new, unsaved order). Desktop clock reads 14:26.

## 92. [35:51-35:51] Display IMG (gui T-code=SPRO)
- Implementation Guide  Edit  Goto  Additional Information  Utilities(M)  System  Help
- Display IMG
- Existing BC Sets | BC Sets for Activity | Activated BC Sets for Activity | Release Notes | Change Log | Where Else Used
- StructureOrder | Net value 4,598.00 EUR
- Serial Numbers
- Routes
- Follow-Up Actions
- Sales
- Sales Documents
- Maintain Copy Control for Sales Documents
- Maintain Display of Date Category and Periods
- Lists
- Set Updating Of Partner Index
- Set Updating Of Item Index
- _(notes)_ Live SAP GUI: IMG (Implementation Guide) structure tree shown in transaction SPRO. The first two header field labels are partly hidden behind the IMG tab strip.

## 93. [36:00-36:01] Create Standard Order: Overview (gui T-code=SPRO)
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Create Standard Order: Overview
- Orders
- Change Plant
- Plant  1000  Dresden
- Standard Order | Net value 4,598.00 EUR
- Sold-to party T-S62130
- Ship-to party Teleko Textilien / Hirschstr. 53 / 55124 Mainz
- PO Number
- Req. deliv. date  D 12.06.2007
- Delivery block | Total Weight 41 KG
- Billing block | Volume 0.000
- Payment card | Pricing date 02.06.2007
- Payment terms ZB01 | Exp.date
- _(notes)_ Composite screen: VA01 order window (menu bar 'Sales document', tab 'Orders') in front with the 'Change Plant' dialog (Plant 1000 Dresden) open; the SPRO/IMG tree (Define Reporting Views, Contract Han

## 94. [37:16-37:16] Overview: Changing of sales documents (slide)
- Overview: Changing of sales documents
- Fast changes in document
- Order
- Concurrent change to several items
- Item 10 | Mat-12 | Plant 1200 | 2000
- Item 20 | Mat-10 | Plant 1200 | 2000
- Fast change of several documents
- Changes using document list
- _(notes)_ Web-based training slide (SAP Education) shown inside an Internet Explorer window. Two-panel illustration: fast change inside one document versus fast change of several documents via the document list

## 95. [37:35-37:36] Blocks (slide)
- Blocks
- Order
- Blocks
- User sets
- Defining
- User sets and removes blocks
- Header
- Delivery block/Billing block
- Item 10
- Billing block
- Item 20
- Schedule line 1
- Schedule line 2
- Delivery block
- _(notes)_ Early/partially revealed web-based training slide titled 'Blocks' (order -> blocks -> user sets -> defining). Illustration labels are small; the visible keywords are listed.

## 96. [38:00-38:00] Change Plant (gui)
- Change Plant
- Plant  1000  Dresden
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Orders
- Item 10
- Billing block
- Item 20
- Schedule line 1
- Schedule line 2
- Delivery block
- Defining blocks in Customizing
- _(notes)_ Composite screenshot: a live SAP GUI 'Change Plant' dialog (with a plant dropdown) floats over the fading 'Blocks' web slide. The status-bar transaction code is not readable in this frame (the video c

## 97. [38:01-38:01] Create Standard Order: Overview (gui T-code=VA01)
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Create Standard Order: Overview
- Sales | Item overview | Customer | Reason for rejection
- Change Plant
- Plant  1000  Dresden
- Standard Order | Net value 4,598.00 EUR
- Sold-to party T-S62130
- Ship-to party Teleko Textilien / Hirschstr. 53 / 55124 Mainz
- PO Number
- Req. deliv. date  D 12.06.2007
- Delivery block | Total Weight 41 KG
- Billing block | Volume 0.000
- Payment card | Pricing date 02.06.2007
- Payment terms ZB01  14 Days 3%, 30/2% | Exp.date
- _(notes)_ Live SAP GUI VA01 order screen with the 'Change Plant' dialog open; the web-based training window is still visible behind the SAP GUI session.

## 98. [38:04-38:04] SAP Logon 710 (gui T-code=VA01)
- SAP Logon 710
- Log On | New | Change | Delete | System Information
- Description
- Manuli Suzhou PR1 outside
- Manuli Suzhou QLE inside
- Manuli Suzhou QLE outside
- NCS - BW
- NCS - Solution Manager
- NCS IDES EC6
- NCS IDES EC6 Internet
- NCS SAP
- NCS SAP Internet
- NCS SG DEV Internet
- NCS SG DEV OFFICE
- _(notes)_ The SAP Logon 710 pad (system list) window is shown on top of the VA01 order screen; the VA01 status bar is still visible. System entries are listed verbatim; one entry is a search result highlighted 

## 99. [38:06-38:48] New password (other T-code=S000)
- New password
- Client
- 904
- User
- Password
- New password
- Repeat password
- Language
- SAP Training System
- SAP S000
- Client 904
- User  tscm6-00
- Password  *******
- Language  EN
- _(notes)_ SAP GUI logon dialog (SAP Logon / SAP GUI for Windows) requesting credentials for system 'SAP Training System'; NOT a lecture slide and not an SAP transaction screen. Status bar reads S000.

## 100. [38:49-38:49] Blocks (slide)
- Blocks
- User sets and removes blocks
- Order
- Header
- Delivery block/Billing block
- Item 10
- Billing block
- Item 20
- Schedule line 1
- Schedule line 2
- Delivery block
- Defining blocks in Customizing
- _(notes)_ Full web-based training slide titled 'Blocks' displayed in an Internet Explorer window (SAP Education banner visible). Same content as t02256.

## 101. [39:43-39:47] SAP Easy Access (gui)
- SAP Easy Access
- Menu  Edit  Favorites  Extras  System  Help
- Other menu
- Create role
- My Customizing Worklist
- Project | Name
- _(notes)_ Live SAP GUI opening screen (SAP Easy Access / session manager) fading in over the web-based training window; the menu tree is not yet rendered and no status bar is visible in this frame.

## 102. [39:48-39:49] Customizing: Execute Project (gui)
- Customizing: Execute Project
- Project  Edit  Goto  Settings  Tools  System  Help
- SAP Reference IMG
- Information
- Project Analysis
- My Customizing Worklist
- Project | Name
- SPRO | tmn03 | OVR
- _(notes)_ Live SAP GUI Customizing (IMG) worklist screen with the 'SAP Reference IMG' button and 'My Customizing Worklist' table. Bottom status bar is cropped in this frame, so the transaction code is not reada

## 103. [39:54-40:00] Display IMG (gui T-code=SPRO)
- Display IMG
- Implementation Guide  Edit  Goto  Additional Information  Utilities(M)  System  Help
- SAP Reference IMG
- SPRO | tmn03 | OVR
- Sales and Distribution
- Master Data
- Basic Functions
- Sales
- Foreign Trade/Customs
- Billing
- Sales Support (CAS)
- Contract Handling
- Pendulum List Indirect Sales
- Electronic Data Interchange
- _(notes)_ Live SAP GUI: the 'Display IMG' structure tree opened from SAP Reference IMG. The tree is scrolled to the top-level nodes; individual node labels are too small to transcribe reliably in this frame.

## 104. [48:01-49:20] Changes to the Sold-to Party in the Sales Document (slide T-code=VA01)
- Changes to the Sold-to Party in the Sales Document
- Redetermined Data
- Customer master
- Customer-material info record
- Unchanged Data
- Sales area
- Sales office and sales group
- Create Standard Order: Overview
- All items
- Item Material Order quantity SU Description S Customer Material Numb ItCa DGi HglVlt D First date Pint Batch
- 10 T-ATA30 1 PC Screen 1 TAN D 09.06.2007 1200
- 20 T-ATA29 1 PC Screen 1 TAN D 09.06.2007 1200
- Req. deliv.date  09.06.2007
- Payment terms  ZB01  14 Days 3%, 30/2%,
- _(notes)_ Slide mid-animation (only 2 redetermination bullets revealed), composited over the live VA01 Create Standard Order: Overview window; status bar VA01 / trn03 / OVR, taskbar clock 14:40.

## 105. [49:35-50:00] Create Standard Order: Overview (gui)
- Sales document  Edit  Goto  Extras  Environment  System  Help
- Orders
- Standard Order
- Sold-to party
- Ship-to party
- PO Number
- Net value  4,598.00 EUR
- PO date
- Becker Berlin / Calvinstrasse 36 / 13467 Berlin-Hermsdorf
- test
- Sales
- Item overview
- Item detail
- Ordering party
- _(notes)_ Data-entry state of the VA01 overview: window title bar and SAP status bar are cropped/not visible in this frame, so no tcode could be read directly; screen layout, tabs, fields and status-bar slot ma

## 106. [50:19-50:19] Create Standard Order: Overview - Customer Change: Initial Screen (gui T-code=VA01)
- Create Standard Order: Overview
- Customer Change: Initial Screen
- Customer
- Company code
- Deliver.Plant
- Sales area
- Sales Organization
- Distribution Channel
- Division
- All sales areas...
- Customer's sales areas...
- Orders
- Sales  Item overview  Item detail  Ordering party  Procurement  Shipping  Reason for rejection
- _(notes)_ Modal 'Customer Change: Initial Screen' dialog opened from the VA01 order (dialog lets the user enter company code, delivering plant and sales area before jumping to the customer master). Status bar V

## 107. [50:48-50:49] Change Customer: General Data (gui T-code=XD02)
- Change Customer: General Data
- Customer  Edit  Goto  Extras  Environment  System  Help
- General Data
- Company Code Data
- Sales Area Data
- Additional Component
- Additional Data
- Empties
- Address
- Control data
- Payment transactions
- Marketing
- Unloading points
- Export data
- _(notes)_ Customer master change (XD02) opened from the order; Address tab selected, first field being edited. Status bar XD02 / trn03 / OVR.

## 108. [50:53-50:53] Change Customer: Sales Area Data (gui T-code=XD02)
- Change Customer: Sales Area Data
- Customer  Edit  Goto  Extras  Environment  System  Help
- Sales
- Shipping
- Billing document
- Partner functions
- Customer  1000
- Becker Berlin
- Berlin
- Sales Org.  1000
- Germany Frankfurt
- Distr. Channel  10
- Final customer sales
- Division  00
- _(notes)_ Sales Area Data, Sales tab for customer 1000. Status bar XD02 / trn03 / OVR.

## 109. [51:10-51:11] Change Customer: Sales Area Data - Partner functions (gui T-code=XD02)
- Change Customer: Sales Area Data
- Sales  Shipping  Billing document  Partner functions
- Customer  1000
- Becker Berlin
- Sales Org.  1000   Distr. Channel  10   Division  00
- Partner Functions
- PF  Partner function  Number  Name  Partner description  D
- SP  Sold-to party  1000  Becker Berlin
- BP  Bill-to party  1000  Becker Berlin
- Delivery and payment terms
- Incoterms
- Terms of payment
- Paym.guar.proc.
- Credit ctrl area
- _(notes)_ Partner functions tab plus Delivery/payment terms, Accounting and Taxes blocks. Status bar XD02 / trn03 / OVR.

## 110. [51:22-51:22] Change Customer: Sales Area Data (gui T-code=XD02)
- Change Customer: Sales Area Data
- Sales  Shipping  Billing document  Partner functions
- Customer  1000
- Becker Berlin
- Sales Org.  1000   Distr. Channel  10   Division  00
- Sales order
- Sales district
- Sales Office
- Sales Group
- Customer group
- ABC class
- Currency
- Switch off rounding
- Order probab.
- _(notes)_ Sales tab re-showed (scrolled so the full Sales order / Pricing/Statistics blocks are visible). Taskbar clock 14:43.

## 111. [51:35-51:40] Change View "Maintain Sales Order Types": Details (gui T-code=VOV8)
- Change View "Maintain Sales Order Types": Details
- Table View  Edit  Goto  Selection  Utilities(M)  System  Help
- Shipping
- Delivery type
- Delivery block
- Shipping conditions
- ShipCostInfoProfile
- Immediate delivery
- Billing
- Dlv-rel.billing type
- Order-rel.bill.type  G2  Credit Memo
- Intercomp.bill.type
- Billing block  08  Check credit memo
- CndType line items
- _(notes)_ Customizing table for sales order types (VOV8, display/change Details screen), scrolled to the Shipping/Billing/date-proposal blocks. Status bar VOV8 / trn03 / OVR.

## 112. [51:42-51:42] Change View "Maintain Sales Order Types": Overview (gui T-code=VOV8)
- Change View "Maintain Sales Order Types": Overview
- Table View  Edit  Goto  Selection  Utilities(M)  System  Help
- New Entries
- SaTy  Description  Block
- CR  Credit Memo Request
- G2N  Credit Memo Req. Val
- GK  Master Contract
- ISBR  B2R: Internet Sales
- ISCC  ISChemComplaint
- ISPO  ISA: Host. Ord. Mgm.
- CP  Consignment Pick-up
- CPC  Consign.Pick-up CompS
- CF  Consignment Fill-up
- KBB  Cons. fill-up BR
- _(notes)_ VOV8 overview table of all sales document types (238 entries); rows CR, G2N, GK, ISBR, ISCC, ISPO, CP, CPC, CF, KBB, CI, KEB, FD, QC, SDF, CONR, CPES, DR, L2DM, L2DP, L2MT, AT, LAB visible. Status bar

## 113. [51:48-52:18] Display IMG (gui T-code=SPRO)
- Display IMG
- Implementation Guide  Edit  Goto  Additional Information  Utilities(M)  System  Help
- Existing BC Sets
- BC Sets for Activity
- Activated BC Sets for Activity
- Release Notes
- Change Log
- Where Else Used
- SAP NetWeaver
- Enterprise Structure
- Cross-Application Components
- Auto-ID Infrastructure
- Financial Accounting
- Financial Supply Chain Management
- _(notes)_ IMG customizing tree (transaction SPRO, Display IMG) opened to Sales and Distribution > Master Data > Basic Functions. Status bar SPRO / trn03 / OVR. Clock 14:44.

## 114. [52:22-52:22] Change View "Customer groups": Overview (gui T-code=OVS9)
- Table View  Edit  Goto  Selection  Utilities(M)  System  Help
- Change View "Customer groups": Overview
- New Entries
- CGrp
- Name
- 01  Industrial customers
- 02  Trading companies
- 03  Development partners
- 04  Wholly-owned subsid.
- 05  Part-owned subsidi.
- 06  Competition
- 07  Public sector
- 10  Private customer
- 20  CP Mass
- _(notes)_ Live SAP GUI table maintenance window (Customizing table view of customer groups, 47 entries) opened over the IMG. Status bar: OVS9 | trn03 | OVR — confirmed at high zoom.

## 115. [52:23-52:48] Display IMG (gui T-code=SPRO)
- Implementation Guide  Edit  Goto  Additional Information  Utilities(M)  System  Help
- Display IMG
- Existing BC Sets
- BC Sets for Activity
- Activated BC Sets for Activity
- Release Notes
- Change Log
- Where Else Used
- Structure
- Auto-ID Infrastructure
- Financial Accounting
- Financial Supply Chain Management
- Controlling
- Investment Management
- _(notes)_ Live SAP GUI IMG. All buttons are now drawn: 'BC Sets for Activity' and 'Activated BC Sets for Activity' appear (they were blank grey in the preceding frames). Tooltip 'Define Customer Groups' is disp

## 116. [52:54-52:55] Change View "Customer Account Groups": Overview (gui T-code=SPRO)
- Table View  Edit  Goto  Choose  Utilities(M)  System  Help
- Change View "Customer Account Groups": Overview
- New entries
- Group
- Name
- 0001  Sold-to party - 0001
- 0002  Goods recipient
- 0003  Payer
- 0004  Bill-to party
- 0005  Prospective customer
- 0006  Competitor
- 0007  Sales partner
- 0008  ...(row partially hidden behind scroll bar)
- Season
- _(notes)_ Live SAP GUI. The customer account-group table maintenance view (OVT0-style overview) is opened in a smaller window on top of the IMG; the status bar shows SPRO / trn03 / OVR, i.e. the IMG session was

## 117. [53:02-53:02] Change View "Customer Account Groups": Details (gui T-code=OVT0)
- Table View  Edit  Goto  Choose  Utilities(M)  System  Help
- Change View "Customer Account Groups": Details
- Expand field status
- New entries
- Account group
- 0001
- Sold-to party - 0001
- General data
- Number range
- 01
- One-time acct
- Field status
- General data
- Company code data
- _(notes)_ Live SAP GUI detail screen of customer account group 0001. Checkboxes Competitors / Sales partner / Prospect / Default SP / Consumer all unchecked; 'One-time acct' unchecked. Status bar: OVT0 / trn03 

## 118. [53:38-53:38] Change View "Customer Account Groups": Details (partially redrawn) (gui T-code=OVT0)
- Table View  Edit  Goto  Choose  Utilities(M)  System  Help
- Performance Assistant
- 0001
- old-
- ld-
- sold-
- 01
- General data
- Field status
- Text proc.
- Sales and distribution data
- Cust.pric.proc.
- PartnDet.Proc.
- OutputDet.Proc.
- _(notes)_ Live SAP GUI, same account-group detail screen as the previous frame but the window is caught mid-repaint: the layout is torn and most labels/values are not rendered (only fragments such as 'old- 0001

## 119. [54:09-54:09] Change View "Customer Account Groups": Details (gui T-code=OVT0)
- Table View  Edit  Goto  Choose  Utilities(M)  System  Help
- Change View "Customer Account Groups": Details
- Expand field status
- New entries
- Account group
- 0001
- Sold-to party - 0001
- General data
- Number range
- 01
- One-time acct
- Field status
- General data
- Company code data
- _(notes)_ Live SAP GUI, account group 0001 detail screen fully rendered again after the repaint. The 'Field status' group now also lists 'Sales data' next to General data / Company code data. All five usage che

## 120. [54:13-54:13] Change Customer: Sales Area Data (gui T-code=XD02)
- Customer  Edit  Goto  Extras  Environment  System  Help
- Change Customer: Sales Area Data
- General Data
- Company Code Data
- Sales Area Data
- Additional Component
- Additional Data
- Empties
- Customer
- 1000
- Becker Berlin
- Berlin
- Sales Org.
- 1000
- _(notes)_ Live SAP GUI customer master change screen, Sales Area Data tab, Sales Order sub-tab. Curator/authorization fields (Authoriz.Group, Item proposal, Units group, Exch. Rate Type, PP cust. proc.) are emp

## 121. [55:13-55:13] Maintain User Profile (gui T-code=SU3)
- Edit  Goto  System  Help
- Maintain User Profile
- Password
- User
- TSCM6-00
- Last Changed On
- TSCM6-00
- 02.06.2007
- 09:22:19
- Status
- Saved
- Defaults
- Parameters
- Address
- _(notes)_ Live SAP GUI user-profile maintenance screen (Address tab). Only identification fields are filled; the header area is mid-repaint so some labels there are unreadable. Status bar: SU3 / trn03 / OVR. Sy

## 122. [55:14-55:14] Maintain User Profile (Parameters tab) (gui T-code=SU3)
- Edit  Goto  System  Help
- Maintain User Profile
- Password
- User
- TSCM6-00
- Last Changed On
- TSCM6-00
- 02.06.2007
- 09:22:19
- Status
- Saved
- Address
- Defaults
- Parameters
- _(notes)_ Live SAP GUI, SU3 Parameters tab showing two user parameter entries. All other rows empty. Status bar: SU3 / trn03 / OVR.

## 123. [55:28-55:28] Maintain User Profile (Favorites / menu tree) (gui T-code=SU3)
- Menu  Edit  Favorites  Extras  System  Help
- Maintain User Profile
- Other menu
- Create role
- Favorites
- SAP menu
- Office
- Cross-Application Components
- Auto-ID Infrastructure
- _(notes)_ Live SAP GUI SU3 Favorites tab: the SAP menu tree is expanded only to the top nodes (Office, Cross-Application Components, Auto-ID Infrastructure). The right-hand area of the window is mid-repaint/tor

## 124. [55:30-55:30] SAP Easy Access (favorites / menu tree) (gui T-code=SU3)
- Menu  Edit  Favorites  Extras  System  Help
- SAP Easy Access
- Other menu
- Create role
- Assign users
- Documentation
- Favorites
- SAP menu
- Office
- Cross-Application Components
- Auto-ID Infrastructure
- _(notes)_ Live SAP GUI. Same tree as the previous frame but the window header now reads 'SAP Easy Access' and a blue water-ripple splash image is drawn in the empty right-hand area (window mid-repaint). Tree no

## 125. [55:33-55:33] (slide fading in — heading not yet legible) (slide T-code=SU3)
- Prices
- Output
- Plant and shipping point
- Batches
- No changes if there are:
- - Status relevant preceding documents
- Subsequent documents
- SAP Easy Access
- Other menu
- Create role
- Favorites
- SAP menu
- Office
- Cross-Application Components
- _(notes)_ Transition frame: a presentation slide is cross-fading in over the live SAP GUI window (the SAP Easy Access screen with the SU3 session is still visible behind/around it). The slide's main heading is 

## 126. [55:34-56:07] Changes to the Sold-to Party in the Sales Document (slide)
- Changes to the Sold-to Party in the Sales Document
- Redetermined Data
- Customer master
- Customer-material info record
- Texts
- Free goods
- Prices
- Output
- Plant and shipping point
- Unchanged Data
- Sales area
- Sales office and sales group
- Availability and product allocation
- Batches
- _(notes)_ Presentation page (browser caption 'SAP Education - Windows Internet Explorer'), fully rendered after the cross-fade. Two-column layout with a blue 'Redetermined Data' box and a green 'Unchanged Data'

## 127. [56:58-56:58] Lesson Summary (slide)
- Lesson Summary
- You should now be able to:
- Find and use the tools and help for entering and processing sales orders
- _(notes)_ Final-section recap page fading in (SAP Education browser deck): heading 'Lesson Summary', lead-in 'You should now be able to:' and the first objective bullet. The remaining bullet text is still disso

## 128. [57:36-57:36] Unit Summary (slide)
- Unit Summary
- You should now be able to:
- Determine the origin of document data ... material master, the customer master, or Customizing
- Find and use the tools and help for e... ers
- NetMeeting - 15 个连接
- 呼叫(C)  查看(V)  工具(T)  帮助(H)
- 共享(S)  Ctrl+S
- 聊天(T)  Ctrl+T
- 白板(W)  Ctrl+W
- 文件传送(F)  Ctrl+F
- 白板 (1.0 - 2.x)
- 远程桌面共享(R)...
- 选项(O)...
- 音频调节向导(A)
- _(notes)_ FINAL frame of the video (57:36). Closing recap page 'Unit Summary' with the objective list; a Windows NetMeeting window (Chinese-localized UI, 15 connections, participant list) is open on top of it a
