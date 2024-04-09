
export default {
    nodeList: ['http://127.0.0.1:5001','http://127.0.0.1:5002'],
    currentNode: 'http://127.0.0.1:5002',
    setNodeList(data){
        this.nodeList = data;
    },
    setCurrentNode(data){
        this.currentNode = data
    }
};