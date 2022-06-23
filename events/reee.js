module.exports = {
    name: 'messageCreate',
    execute(client) {
        console.log('user has sent a message');
        if (client.messageCreate.content.includes('reee')) {
            const channel = client.channels.cache.get('id');
            channel.send('reee');
        }
    },
};