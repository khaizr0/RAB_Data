require('dotenv').config({ path: require('path').join(__dirname, '..', '.env') });
const { ScanCommand } = require('@aws-sdk/lib-dynamodb');
const { ListTablesCommand } = require('@aws-sdk/client-dynamodb');
const { client, docClient } = require('../config/dynamodb');
const fs = require('fs');
const path = require('path');

async function backupData() {
    console.log('Scanning tables...');
    const { TableNames } = await client.send(new ListTablesCommand({}));
    console.log(`Found ${TableNames.length} tables\n`);
    
    const backup = {};
    
    for (const tableName of TableNames) {
        try {
            const result = await docClient.send(new ScanCommand({ TableName: tableName }));
            backup[tableName] = result.Items || [];
            console.log(`✓ Backed up ${tableName}: ${backup[tableName].length} items`);
        } catch (error) {
            console.error(`✗ Error backing up ${tableName}:`, error.message);
            backup[tableName] = [];
        }
    }
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = path.join(__dirname, `backup-${timestamp}.json`);
    
    fs.writeFileSync(filename, JSON.stringify(backup, null, 2));
    console.log(`\n✓ Backup completed: ${path.basename(filename)}`);
    console.log(`  Location: ${filename}`);
}

backupData();
