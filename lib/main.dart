import 'package:flutter/material.dart';
import 'package:fluentui_system_icons/fluentui_system_icons.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  bool isDarkMode = true;

  void toggleTheme() {
    setState(() {
      isDarkMode = !isDarkMode;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Secure Vault',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: Color(0xFF0078D4),
          brightness: Brightness.light,
        ),
        cardTheme: CardThemeData(
          elevation: 2,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
          surfaceTintColor: null,
          color: ColorScheme.fromSeed(
            seedColor: Color(0xFF0078D4),
          ).surfaceContainerLow,
        ),
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: Color(0xFF0078D4),
          brightness: Brightness.dark,
        ),
        cardTheme: CardThemeData(
          elevation: 2,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
          surfaceTintColor: null,
          color: ColorScheme.fromSeed(
            seedColor: Color(0xFF0078D4),
            brightness: Brightness.dark,
          ).surfaceContainerLow,
        ),
      ),
      themeMode: isDarkMode ? ThemeMode.dark : ThemeMode.light,
      home: SecureVaultScreen(
        onThemeToggle: toggleTheme,
        isDarkMode: isDarkMode,
      ),
      debugShowCheckedModeBanner: false,
    );
  }
}

abstract class VaultPage extends StatelessWidget {
  final String title;
  VaultPage(this.title);
}

class HomePage extends VaultPage {
  HomePage() : super("Home");

  @override
  Widget build(BuildContext context) {
    return _buildDropZonePage(context);
  }

  Widget _buildDropZonePage(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final screenHeight = MediaQuery.of(context).size.height;

    return SingleChildScrollView(
      child: Container(
        height:
            screenHeight - kToolbarHeight - MediaQuery.of(context).padding.top,
        padding: EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              height: screenHeight * 0.35,
              width: double.infinity,
              decoration: BoxDecoration(
                border: Border.all(
                  color: colorScheme.outline.withOpacity(0.6),
                  width: 2,
                ),
                borderRadius: BorderRadius.circular(12),
              ),
              child: InkWell(
                borderRadius: BorderRadius.circular(12),
                onTap: () => _showFilePickerDialog(context),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Container(
                      padding: EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: colorScheme.primaryContainer.withOpacity(0.3),
                        shape: BoxShape.circle,
                      ),
                      child: Icon(
                        FluentIcons.cloud_arrow_up_24_regular,
                        size: 48,
                        color: colorScheme.primary,
                      ),
                    ),
                    SizedBox(height: 20),
                    Text(
                      "Drag and Drop Files or Folders Here",
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.w600,
                        fontSize: 20,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    SizedBox(height: 12),
                    Text(
                      "or Click to Select",
                      style: Theme.of(
                        context,
                      ).textTheme.bodyLarge?.copyWith(fontSize: 16),
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(height: 24),
            Container(
              padding: EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: colorScheme.surfaceContainer,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "Recent Files",
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.w600,
                      fontSize: 18,
                    ),
                  ),
                  SizedBox(height: 16),
                  _buildFileItem(context, "New Text Document - Copy (2).txt"),
                ],
              ),
            ),
            Expanded(
              child: Align(
                alignment: Alignment.bottomCenter,
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Row(
                      children: [
                        Expanded(
                          child: _buildActionButton(
                            context,
                            "Open Folder",
                            FluentIcons.folder_open_24_regular,
                          ),
                        ),
                        SizedBox(width: 12),
                        Expanded(
                          child: _buildActionButton(
                            context,
                            "Lock Folder",
                            FluentIcons.lock_closed_24_regular,
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 12),
                    Row(
                      children: [
                        Expanded(
                          child: _buildActionButton(
                            context,
                            "Unlock Folder",
                            FluentIcons.lock_open_24_regular,
                          ),
                        ),
                        SizedBox(width: 12),
                        Expanded(
                          child: _buildActionButton(
                            context,
                            "Secure Delete",
                            FluentIcons.delete_24_regular,
                            isDestructive: true,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFileItem(BuildContext context, String fileName) {
    return Card(
      margin: EdgeInsets.only(bottom: 8),
      child: ListTile(
        contentPadding: EdgeInsets.all(12),
        leading: Container(
          width: 40,
          height: 40,
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.primaryContainer,
            borderRadius: BorderRadius.circular(8),
          ),
          child: Icon(
            FluentIcons.document_24_regular,
            color: Theme.of(context).colorScheme.onPrimaryContainer,
            size: 20,
          ),
        ),
        title: Text(
          fileName,
          style: TextStyle(fontSize: 14, fontWeight: FontWeight.w500),
        ),
        subtitle: Text(
          "Uncategorized • Modified today",
          style: TextStyle(fontSize: 12),
        ),
        trailing: Container(
          width: 36,
          height: 36,
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.surfaceVariant,
            borderRadius: BorderRadius.circular(8),
          ),
          child: PopupMenuButton(
            icon: Icon(FluentIcons.more_vertical_24_regular, size: 18),
            itemBuilder: (context) => [
              PopupMenuItem(
                child: Text("Open", style: TextStyle(fontSize: 14)),
                value: "open",
              ),
              PopupMenuItem(
                child: Text("Rename", style: TextStyle(fontSize: 14)),
                value: "rename",
              ),
              PopupMenuItem(
                child: Text("Delete", style: TextStyle(fontSize: 14)),
                value: "delete",
              ),
            ],
          ),
        ),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      ),
    );
  }

  Widget _buildActionButton(
    BuildContext context,
    String text,
    IconData icon, {
    bool isDestructive = false,
  }) {
    return SizedBox(
      height: 48,
      child: isDestructive
          ? FilledButton.tonal(
              onPressed: () => _handleAction(context, text),
              style: FilledButton.styleFrom(
                backgroundColor: Theme.of(context).colorScheme.errorContainer,
                foregroundColor: Theme.of(context).colorScheme.onErrorContainer,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                textStyle: TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(icon, size: 18),
                  SizedBox(width: 8),
                  Text(text),
                ],
              ),
            )
          : FilledButton(
              onPressed: () => _handleAction(context, text),
              style: FilledButton.styleFrom(
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                textStyle: TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(icon, size: 18),
                  SizedBox(width: 8),
                  Text(text),
                ],
              ),
            ),
    );
  }

  void _handleAction(BuildContext context, String action) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('$action pressed'),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(6)),
      ),
    );
  }

  void _showFilePickerDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Select Files'),
          content: Text(
            'File picker would open here in a real implementation.',
          ),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
          actions: [
            TextButton(
              child: Text('Cancel'),
              onPressed: () => Navigator.of(context).pop(),
            ),
            FilledButton(
              child: Text('Select'),
              onPressed: () => Navigator.of(context).pop(),
            ),
          ],
        );
      },
    );
  }
}

class SettingsPage extends VaultPage {
  SettingsPage() : super("Settings");

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    return Padding(
      padding: EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: colorScheme.primaryContainer.withOpacity(0.3),
                  shape: BoxShape.circle,
                ),
                child: Icon(
                  FluentIcons.settings_24_regular,
                  size: 32,
                  color: colorScheme.primary,
                ),
              ),
              SizedBox(width: 12),
              Text(
                "Settings",
                style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.w700,
                  fontSize: 24,
                  color: colorScheme.onSurface,
                ),
              ),
            ],
          ),
          SizedBox(height: 24),
          Expanded(
            child: ListView(
              children: [
                Card(
                  elevation: 4,
                  child: Padding(
                    padding: EdgeInsets.all(8),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Padding(
                          padding: EdgeInsets.symmetric(
                            horizontal: 12,
                            vertical: 8,
                          ),
                          child: Text(
                            "General",
                            style: Theme.of(context).textTheme.titleMedium
                                ?.copyWith(
                                  fontWeight: FontWeight.w600,
                                  fontSize: 18,
                                  color: colorScheme.onSurface,
                                ),
                          ),
                        ),
                        ListTile(
                          leading: Icon(
                            FluentIcons.shield_24_regular,
                            size: 24,
                            color: colorScheme.primary,
                          ),
                          title: Text(
                            "Security",
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          subtitle: Text(
                            "Manage encryption and access controls",
                            style: TextStyle(
                              fontSize: 14,
                              color: colorScheme.onSurfaceVariant,
                            ),
                          ),
                          trailing: Icon(
                            FluentIcons.chevron_right_24_regular,
                            size: 20,
                            color: colorScheme.onSurfaceVariant,
                          ),
                          onTap: () {},
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                        ),
                        Divider(height: 1, indent: 12, endIndent: 12),
                        ListTile(
                          leading: Icon(
                            FluentIcons.cloud_sync_24_regular,
                            size: 24,
                            color: colorScheme.primary,
                          ),
                          title: Text(
                            "Backup",
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          subtitle: Text(
                            "Configure automatic backups",
                            style: TextStyle(
                              fontSize: 14,
                              color: colorScheme.onSurfaceVariant,
                            ),
                          ),
                          trailing: Switch(
                            value: true,
                            onChanged: (value) {},
                            activeColor: colorScheme.primary,
                          ),
                          onTap: () {},
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                        ),
                        Divider(height: 1, indent: 12, endIndent: 12),
                        ListTile(
                          leading: Icon(
                            FluentIcons.storage_24_regular,
                            size: 24,
                            color: colorScheme.primary,
                          ),
                          title: Text(
                            "Storage",
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          subtitle: Text(
                            "Manage storage locations",
                            style: TextStyle(
                              fontSize: 14,
                              color: colorScheme.onSurfaceVariant,
                            ),
                          ),
                          trailing: Icon(
                            FluentIcons.chevron_right_24_regular,
                            size: 20,
                            color: colorScheme.onSurfaceVariant,
                          ),
                          onTap: () {},
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                SizedBox(height: 16),
                Card(
                  elevation: 4,
                  child: Padding(
                    padding: EdgeInsets.all(8),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Padding(
                          padding: EdgeInsets.symmetric(
                            horizontal: 12,
                            vertical: 8,
                          ),
                          child: Text(
                            "System",
                            style: Theme.of(context).textTheme.titleMedium
                                ?.copyWith(
                                  fontWeight: FontWeight.w600,
                                  fontSize: 18,
                                  color: colorScheme.onSurface,
                                ),
                          ),
                        ),
                        ListTile(
                          leading: Icon(
                            FluentIcons.alert_24_regular,
                            size: 24,
                            color: colorScheme.primary,
                          ),
                          title: Text(
                            "Notifications",
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          subtitle: Text(
                            "Configure alert settings",
                            style: TextStyle(
                              fontSize: 14,
                              color: colorScheme.onSurfaceVariant,
                            ),
                          ),
                          trailing: Switch(
                            value: false,
                            onChanged: (value) {},
                            activeColor: colorScheme.primary,
                          ),
                          onTap: () {},
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                        ),
                        Divider(height: 1, indent: 12, endIndent: 12),
                        ListTile(
                          leading: Icon(
                            FluentIcons.info_24_regular,
                            size: 24,
                            color: colorScheme.primary,
                          ),
                          title: Text(
                            "About",
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          subtitle: Text(
                            "Version 1.0.0",
                            style: TextStyle(
                              fontSize: 14,
                              color: colorScheme.onSurfaceVariant,
                            ),
                          ),
                          trailing: Icon(
                            FluentIcons.chevron_right_24_regular,
                            size: 20,
                            color: colorScheme.onSurfaceVariant,
                          ),
                          onTap: () {},
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class SecureVaultScreen extends StatefulWidget {
  final VoidCallback onThemeToggle;
  final bool isDarkMode;

  SecureVaultScreen({required this.onThemeToggle, required this.isDarkMode});

  @override
  _SecureVaultScreenState createState() => _SecureVaultScreenState();
}

class _SecureVaultScreenState extends State<SecureVaultScreen> {
  int selectedNavIndex = 0;

  final List<VaultPage> pages = [HomePage(), SettingsPage()];

  final List<NavigationItem> navItems = [
    NavigationItem(FluentIcons.home_24_regular, "Home"),
    NavigationItem(FluentIcons.settings_24_regular, "Settings"),
  ];

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final isWideScreen = MediaQuery.of(context).size.width > 800;

    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Icon(FluentIcons.shield_24_regular, color: colorScheme.primary),
            SizedBox(width: 8),
            Text('Secure Vault', style: TextStyle(fontWeight: FontWeight.w600)),
          ],
        ),
        actions: [
          FilledButton.tonal(
            onPressed: widget.onThemeToggle,
            style: FilledButton.styleFrom(
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(7),
              ),
            ),
            child: Text(widget.isDarkMode ? 'Light' : 'Dark'),
          ),
          SizedBox(width: 12),
        ],
      ),
      drawer: isWideScreen ? null : _buildDrawer(),
      body: isWideScreen ? _buildWideScreenLayout() : pages[selectedNavIndex],
      bottomNavigationBar: isWideScreen ? null : _buildBottomNavBar(),
    );
  }

  Widget _buildWideScreenLayout() {
    return Row(
      children: [
        Card(
          margin: EdgeInsets.all(8),
          child: Container(
            width: 240,
            padding: EdgeInsets.all(8),
            child: Column(
              children: [
                Expanded(
                  child: Column(
                    children: [
                      Expanded(
                        child: ListView.builder(
                          padding: EdgeInsets.symmetric(horizontal: 8),
                          itemCount: navItems.length - 1,
                          itemBuilder: (context, index) {
                            final isSelected = selectedNavIndex == index;
                            return Container(
                              margin: EdgeInsets.symmetric(vertical: 4),
                              child: ListTile(
                                leading: Icon(
                                  navItems[index].icon,
                                  color: isSelected
                                      ? Theme.of(context).colorScheme.primary
                                      : Theme.of(
                                          context,
                                        ).colorScheme.onSurfaceVariant,
                                ),
                                title: Text(
                                  navItems[index].title,
                                  style: TextStyle(
                                    fontWeight: isSelected
                                        ? FontWeight.w600
                                        : FontWeight.normal,
                                  ),
                                ),
                                selected: isSelected,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                onTap: () {
                                  setState(() {
                                    selectedNavIndex = index;
                                  });
                                },
                              ),
                            );
                          },
                        ),
                      ),
                      Container(
                        margin: EdgeInsets.symmetric(
                          vertical: 4,
                          horizontal: 8,
                        ),
                        child: ListTile(
                          leading: Icon(
                            navItems.last.icon,
                            color: selectedNavIndex == navItems.length - 1
                                ? Theme.of(context).colorScheme.primary
                                : Theme.of(
                                    context,
                                  ).colorScheme.onSurfaceVariant,
                          ),
                          title: Text(
                            navItems.last.title,
                            style: TextStyle(
                              fontWeight:
                                  selectedNavIndex == navItems.length - 1
                                  ? FontWeight.w600
                                  : FontWeight.normal,
                            ),
                          ),
                          selected: selectedNavIndex == navItems.length - 1,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                          onTap: () {
                            setState(() {
                              selectedNavIndex = navItems.length - 1;
                            });
                          },
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
        Expanded(
          child: Card(
            margin: EdgeInsets.fromLTRB(0, 8, 8, 8),
            child: pages[selectedNavIndex],
          ),
        ),
      ],
    );
  }

  Widget _buildDrawer() {
    return NavigationDrawer(
      selectedIndex: selectedNavIndex,
      onDestinationSelected: (index) {
        setState(() {
          selectedNavIndex = index;
        });
        Navigator.pop(context);
      },
      children: [
        Padding(
          padding: EdgeInsets.fromLTRB(28, 16, 16, 10),
          child: Text(
            'Navigation',
            style: Theme.of(context).textTheme.titleSmall,
          ),
        ),
        ...navItems.asMap().entries.map((entry) {
          return NavigationDrawerDestination(
            icon: Icon(entry.value.icon),
            label: Text(entry.value.title),
          );
        }).toList(),
      ],
    );
  }

  Widget _buildBottomNavBar() {
    return NavigationBar(
      selectedIndex: selectedNavIndex,
      onDestinationSelected: (index) {
        setState(() {
          selectedNavIndex = index;
        });
      },
      destinations: navItems.map((item) {
        return NavigationDestination(icon: Icon(item.icon), label: item.title);
      }).toList(),
    );
  }
}

class NavigationItem {
  final IconData icon;
  final String title;

  NavigationItem(this.icon, this.title);
}
