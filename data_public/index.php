<?php
header("Content-type:text/html;charset=utf8");
//define your token
define("TOKEN", "omnilab");
date_default_timezone_set(PRC);

$wechatObj = new wechatCallbackapiTest();
$wechatObj->responseMsg();
//$wechatObj->valid();

class wechatCallbackapiTest
{  
    public function valid()
    {
        $echoStr = $_GET["echostr"];

        if($this->checkSignature()){
            echo $echoStr;
            exit;
        }
    }
    private function checkSignature()
    {   
        if (!defined("TOKEN")) {
            throw new Exception('TOKEN is not defined!');
        }
        
        $signature = $_GET["signature"];
        $timestamp = $_GET["timestamp"];
        $nonce = $_GET["nonce"];    
                
        $token = TOKEN;
        $tmpArr = array($token, $timestamp, $nonce);
        sort($tmpArr);
        $tmpStr = implode( $tmpArr );
        $tmpStr = sha1( $tmpStr );
        
        if( $tmpStr == $signature ){
            return true;
        }else{
            return false;
        }
    }
    
    public function responseMsg()
    {
        $postStr = $GLOBALS["HTTP_RAW_POST_DATA"];

        if (!empty($postStr)){
            libxml_disable_entity_loader(true);
            $postObj = simplexml_load_string($postStr, 'SimpleXMLElement', LIBXML_NOCDATA);
            
            $fromUsername = $postObj->FromUserName;
            $toUsername = $postObj->ToUserName;
            $time = time();
            $msgType = $postObj->MsgType;

            $main = "* 回复数字选择要进行的操作：\n1 数据集记录人工标注\n2 数据集记录标注更改\n3 修改个人昵称\n4 查看标注排行榜前十名";
            
            $mysql = new SaeMysql();
            mysql_set_charset("gbk");

            $newsID = "d86cbf57-3df6-425c-9520-1bf65342ec1d";
            $weiboID = "ca77af73-f179-445d-964c-bbf118ae1b7c";
            
            $textTpl = "<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[%s]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            <FuncFlag>0</FuncFlag>
            </xml>";     
            
            switch ($msgType){
                case 'text':
                    $keyword = trim($postObj->Content);
                    $sql = "select state, count, record_id, perCount from user where fromUsername = '$fromUsername'";
                    $result = $mysql->getData($sql);
                    $state = $result[0]['state'];
                    $count = $result[0]['count'];
                    $record_id = $result[0]['record_id'];
                    $perCount = $result[0]['perCount'];

                    switch ($state) {
                        case 0:
                            switch ($keyword) {
                                case '1':
                                    $sql = "update user set state = '1' where fromUsername = '$fromUsername'";
                                    $mysql->runSql($sql);
                                    $contentStr = "* 回复数字选择要标注的数据集：\n1 微博数据集人工标注\n2 新闻数据集人工标注";
                                    $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                    echo $resultStr;
                                    break;
                                case '2':
                                    $sql = "update user set state = '2' where fromUsername = '$fromUsername'";
                                    $mysql->runSql($sql);
                                    $contentStr = "* 回复数字选择要更改的数据集：\n1 微博数据集标注更改\n2 新闻数据集标注更改";
                                    $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                    echo $resultStr;
                                    break;
                                case '3':
                                    $sql = "update user set state = '3' where fromUsername = '$fromUsername'";
                                    $mysql->runSql($sql);
                                    $contentStr = "* 输入新的昵称：";
                                    $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                    echo $resultStr;
                                    break;
                                case '4':
                                    $sql = "select * from user order by count desc limit 10";
                                    $all = $mysql->getData($sql);
                                    $rank = 1;
                                    $contentStr = "";
                                    while($all[$rank-1]){
                                        $contentStr .= "第".$rank."名： ".$all[$rank-1]['nickname']."[".$all[$rank-1]['count']."]\n";
                                        $rank += 1; 
                                    }
                                    $contentStr .= $main;
                                    $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                    echo $resultStr;
                                    break;
                                default:
                                    $contentStr = "* 信息输入有误，请重新选择操作！\n".$main;
                                    $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                    echo $resultStr;
                                    break;
                            }
                            break;

                        case 1:
                            switch ($keyword) {
                                case '1':
                                    $post_string = '{"limit":1,"sort":"num asc","resource_id":"'.$weiboID.'","filters":{"checked": 0},"offset":'.rand(0,19).'}';
                                    $remote_server = 'http://202.121.178.242/api/3/action/datastore_search';
                                    $context = array(
                                        'http'=>array(
                                            'method'=>'POST',
                                            'header'=>'Authorization: a6c2ce2d-9e11-4be0-9ffb-ffe4966ed9e2',
                                            'content'=>$post_string)
                                    );
                                    $stream_context = stream_context_create( $context );
                                    $data = json_decode( file_get_contents( $remote_server, FALSE, $stream_context ), true );
                                    $result = $data['result']['records'][0];
                                    
                                    $num = $result['num'];
                                    $cid = $result['cid'];
                                    $content = $result['content'];

                                    $contentStr = "* 微博序号：$num\n* 内容：$content\n———————————————\n* 请输入标注类别：0 无关信息  1 公交爆炸  2 暴恐  3 校园砍杀  q 退出";
                                    $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                    echo $resultStr;

                                    $sql = "update user set state = '11',record_id = '$num' where fromUsername = '$fromUsername'";
                                    $mysql->runSql($sql);

                                    break;

                                case '2':
                                    $post_string = '{"limit":1,"sort":"num asc","resource_id":"'.$newsID.'","filters":{"checked": 0},"offset":'.rand(0,19).'}';
                                    $remote_server = 'http://202.121.178.242/api/3/action/datastore_search';
                                    $context = array(
                                        'http'=>array(
                                            'method'=>'POST',
                                            'header'=>'Authorization: a6c2ce2d-9e11-4be0-9ffb-ffe4966ed9e2',
                                            'content'=>$post_string)
                                    );
                                    $stream_context = stream_context_create( $context );
                                    $data = json_decode( file_get_contents( $remote_server, FALSE, $stream_context ), true );
                                    $result = $data['result']['records'][0];
                                    
                                    $num = $result['num'];
                                    $cid = $result['cid'];
                                    $title = $result['title'];
                                    $content = $result['content'];

                                    $contentStr = "* 新闻序号：$num\n* 标题：$title\n* 内容：$content\n———————————————\n* 请输入标注类别：0 无关信息  1 公交爆炸  2 暴恐  3 校园砍杀  q 退出";
                                    $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                    echo $resultStr;

                                    $sql = "update user set state = '12',record_id = '$num' where fromUsername = '$fromUsername'";
                                    $mysql->runSql($sql);

                                    break;
                                
                                default:
                                    $contentStr = "* 信息输入有误，请重新选择数据集！\n* 回复数字选择要标注的数据集：\n1 微博数据集人工标注\n2 新闻数据集人工标注";
                                    $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                    echo $resultStr;
                                    break;
                            }
                            break;

                        case 11:
                            if($keyword == 'q' || $keyword == 'Q'){
                                $sql = "select * from user order by count desc";
                                $all = $mysql->getData($sql);
                                $rank = 1;
                                while($all[$rank-1]['fromUsername']!=$fromUsername)$rank += 1; 
                                
                                if($rank > 1){
                                    $gap = $all[$rank-2]['count'] - $all[$rank-1]['count'];
                                    $chasename = $all[$rank-2]['nickname'];
                                    $contentStr = "* 退出标注\n* 本次标注量：$perCount\n* 总计标注量：$count\n* 当前排名：$rank\n* 再标注".$gap."项记录即可超过一名小伙伴，".$chasename."！\n";
                                }else{
                                    $contentStr = "* 退出标注\n* 本次标注量：$perCount\n* 总计标注量：$count\n* 当前排名：$rank\n* 你已经是排名第一的标注大师了！继续保持！\n";
                                }
                                $contentStr .= $main;
                                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                echo $resultStr;

                                $sql = "update user set state = '0',record_id = '0',count = '$count',perCount = '0' where fromUsername = '$fromUsername'";
                                $mysql->runSql($sql);

                            }else if( $keyword == '1' || $keyword == '2' || $keyword == '3' || $keyword == '0') {
                                $post_string = '{"force":true,"method":"upsert","resource_id":"'.$weiboID.'","records":[{"num":"'.$record_id.'","checked":"1","hit_tag":"'.$keyword.'"}]}';
                                $remote_server = 'http://202.121.178.242/api/3/action/datastore_upsert';
                                $context = array(
                                    'http'=>array(
                                        'method'=>'POST',
                                        'header'=>'Authorization: a6c2ce2d-9e11-4be0-9ffb-ffe4966ed9e2',
                                        'content'=>$post_string)
                                );
                                $stream_context = stream_context_create( $context );
                                $data = json_decode( file_get_contents( $remote_server, FALSE, $stream_context ), true );
                                $contentStr = "* 您已成功标注一条微博记录！\n";
                                $count = $count + 1;
                                $perCount = $perCount + 1;

                                $post_string = '{"limit":1,"sort":"num asc","resource_id":"'.$weiboID.'","filters":{"checked": 0},"offset":'.rand(0,19).'}';
                                $remote_server = 'http://202.121.178.242/api/3/action/datastore_search';
                                $context = array(
                                    'http'=>array(
                                        'method'=>'POST',
                                        'header'=>'Authorization: a6c2ce2d-9e11-4be0-9ffb-ffe4966ed9e2',
                                        'content'=>$post_string)
                                );
                                $stream_context = stream_context_create( $context );
                                $data = json_decode( file_get_contents( $remote_server, FALSE, $stream_context ), true );
                                $result = $data['result']['records'][0];
                                    
                                $num = $result['num'];
                                $cid = $result['cid'];
                                $content = $result['content'];

                                $contentStr .= "* 微博序号：$num\n* 内容：$content\n———————————————\n* 请输入标注类别：0 无关信息  1 公交爆炸  2 暴恐  3 校园砍杀  q 退出";
                                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                echo $resultStr;

                                $sql = "update user set record_id = '$num',count = '$count',perCount = '$perCount' where fromUsername = '$fromUsername'";
                                $mysql->runSql($sql);

                            }else{
                                $contentStr = "* 信息输入有误，请重新标注！\n* 请输入标注类别：0 无关信息  1 公交爆炸  2 暴恐  3 校园砍杀  q 退出";
                                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                echo $resultStr;
                            }
                            break;

                        case 12:
                             if($keyword == 'q' || $keyword == 'Q'){
                                $sql = "select * from user order by count desc";
                                $all = $mysql->getData($sql);
                                $rank = 1;
                                while($all[$rank-1]['fromUsername']!=$fromUsername)$rank += 1; 
                                
                                if($rank > 1){
                                    $gap = $all[$rank-2]['count'] - $all[$rank-1]['count'];
                                    $chasename = $all[$rank-2]['nickname'];
                                    $contentStr = "* 退出标注\n* 本次标注量：$perCount\n* 总计标注量：$count\n* 当前排名：$rank\n* 再标注".$gap."项记录即可超过一名小伙伴，".$chasename."！\n";
                                }else{
                                    $contentStr = "* 退出标注\n* 本次标注量：$perCount\n* 总计标注量：$count\n* 当前排名：$rank\n* 你已经是排名第一的标注大师了！继续保持！\n";
                                }
                                $contentStr .= $main;
                                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                echo $resultStr;

                                $sql = "update user set state = '0',record_id = '0',count = '$count',perCount = '0' where fromUsername = '$fromUsername'";
                                $mysql->runSql($sql);
                            }else if( $keyword == '1' || $keyword == '2' || $keyword == '3' || $keyword == '0') {
                                $post_string = '{"force":true,"method":"upsert","resource_id":"'.$newsID.'","records":[{"num":"'.$record_id.'","checked":"1","hit_tag":"'.$keyword.'"}]}';
                                $remote_server = 'http://202.121.178.242/api/3/action/datastore_upsert';
                                $context = array(
                                    'http'=>array(
                                        'method'=>'POST',
                                        'header'=>'Authorization: a6c2ce2d-9e11-4be0-9ffb-ffe4966ed9e2',
                                        'content'=>$post_string)
                                );
                                $stream_context = stream_context_create( $context );
                                $data = json_decode( file_get_contents( $remote_server, FALSE, $stream_context ), true );
                                $contentStr = "* 您已成功标注一条新闻记录！\n";
                                $count = $count + 1;
                                $perCount = $perCount + 1;

                                $post_string = '{"limit":1,"sort":"num asc","resource_id":"'.$newsID.'","filters":{"checked": 0},"offset":'.rand(0,19).'}';
                                $remote_server = 'http://202.121.178.242/api/3/action/datastore_search';
                                $context = array(
                                    'http'=>array(
                                        'method'=>'POST',
                                        'header'=>'Authorization: a6c2ce2d-9e11-4be0-9ffb-ffe4966ed9e2',
                                        'content'=>$post_string)
                                );
                                $stream_context = stream_context_create( $context );
                                $data = json_decode( file_get_contents( $remote_server, FALSE, $stream_context ), true );
                                $result = $data['result']['records'][0];
                                    
                                $num = $result['num'];
                                $cid = $result['cid'];
                                $title = $result['title'];
                                $content = $result['content'];

                                $contentStr .= "* 新闻序号：$num\n* 标题：$title\n* 内容：$content\n———————————————\n* 请输入标注类别：0 无关信息  1 公交爆炸  2 暴恐  3 校园砍杀  q 退出";
                                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                echo $resultStr;

                                $sql = "update user set record_id = '$num',count = '$count',perCount = '$perCount' where fromUsername = '$fromUsername'";
                                $mysql->runSql($sql);
                            }else{
                                $contentStr = "* 信息输入有误，请重新标注！\n* 请输入标注类别：0 无关信息  1 公交爆炸  2 暴恐  3 校园砍杀  q 退出";
                                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                echo $resultStr;
                                $sql = "update user set state = '0',record_id = '0' where fromUsername = '$fromUsername'";
                                $mysql->runSql($sql)
                            }
                            break;

                        case 2:
                            switch ($keyword) {
                                case '1':
                                    $contentStr = "* 请输入需要更改的微博记录对应num：";
                                    $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                    echo $resultStr;

                                    $sql = "update user set state = '21' where fromUsername = '$fromUsername'";
                                    $mysql->runSql($sql);

                                    break;

                                case '2':
                                    $contentStr = "* 请输入需要更改的新闻记录对应num：";
                                    $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                    echo $resultStr;

                                    $sql = "update user set state = '22' where fromUsername = '$fromUsername'";
                                    $mysql->runSql($sql);

                                    break;
                                
                                default:
                                    $contentStr = "* 信息输入有误，请重新选择数据集！\n* 回复数字选择要更改的数据集：\n1 微博数据集标注更改\n2 新闻数据集标注更改";
                                    $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                    echo $resultStr;
                                    break;
                            }
                            break;
                        case 21:
                            $post_string = '{"resource_id":"'.$weiboID.'","filters":{"checked": 1,"num":"'.$keyword.'"}}';
                            $remote_server = 'http://202.121.178.242/api/3/action/datastore_search';
                            $context = array(
                                'http'=>array(
                                    'method'=>'POST',
                                    'header'=>'Authorization: a6c2ce2d-9e11-4be0-9ffb-ffe4966ed9e2',
                                    'content'=>$post_string)
                            );
                            $stream_context = stream_context_create( $context );
                            $data = json_decode( file_get_contents( $remote_server, FALSE, $stream_context ), true );
                            if(count($data['result']['records']) > 0){
                                $result = $data['result']['records'][0];
                                    
                                $num = $result['num'];
                                $cid = $result['cid'];
                                $content = $result['content'];

                                $contentStr = "* 请确认微博记录并更改标注\n* 微博序号：$num\n* 内容：$content\n———————————————\n请输入标注类别：0 无关信息  1 公交爆炸  2 暴恐  3 校园砍杀  q 退出";
                                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                echo $resultStr;

                                $sql = "update user set state = '210',record_id = '$num' where fromUsername = '$fromUsername'";
                                $mysql->runSql($sql);
                            }else{
                                $contentStr = "* 不存在对应该num的已标注微博记录！\n* 请再次输入需要更改的微博记录对应num：";
                                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                echo $resultStr;
                            }
                            break;
                        case 210:
                            if($keyword == 'q' || $keyword == 'Q'){
                                $contentStr = "* 您选择了取消更改\n";
                                $contentStr .= $main;
                                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                echo $resultStr;

                                $sql = "update user set state = '0',record_id = '0' where fromUsername = '$fromUsername'";
                                $mysql->runSql($sql);

                            }else if( $keyword == '1' || $keyword == '2' || $keyword == '3' || $keyword == '0') {
                                $post_string = '{"force":true,"method":"upsert","resource_id":"'.$weiboID.'","records":[{"num":"'.$record_id.'","hit_tag":"'.$keyword.'"}]}';
                                $remote_server = 'http://202.121.178.242/api/3/action/datastore_upsert';
                                $context = array(
                                    'http'=>array(
                                        'method'=>'POST',
                                        'header'=>'Authorization: a6c2ce2d-9e11-4be0-9ffb-ffe4966ed9e2',
                                        'content'=>$post_string)
                                );
                                $stream_context = stream_context_create( $context );
                                $data = json_decode( file_get_contents( $remote_server, FALSE, $stream_context ), true );
                                $contentStr = "* 您已成功更改一条微博记录！\n".$main;

                                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                echo $resultStr;

                                $sql = "update user set state = '0', record_id = '0' where fromUsername = '$fromUsername'";
                                $mysql->runSql($sql);

                            }else{
                                $contentStr = "* 信息输入有误，请重新更改！\n* 请输入标注类别：0 无关信息  1 公交爆炸  2 暴恐  3 校园砍杀  q 退出";
                                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                echo $resultStr;
                            }
                            break;

                        case 22:
                            $post_string = '{"resource_id":"'.$newsID.'","filters":{"checked": 1,"num":"'.$keyword.'"}}';
                            $remote_server = 'http://202.121.178.242/api/3/action/datastore_search';
                            $context = array(
                                'http'=>array(
                                    'method'=>'POST',
                                    'header'=>'Authorization: a6c2ce2d-9e11-4be0-9ffb-ffe4966ed9e2',
                                    'content'=>$post_string)
                            );
                            $stream_context = stream_context_create( $context );
                            $data = json_decode( file_get_contents( $remote_server, FALSE, $stream_context ), true );
                            if(count($data['result']['records']) > 0){
                                $result = $data['result']['records'][0];
                                    
                                $num = $result['num'];
                                $cid = $result['cid'];
                                $title = $result['title'];
                                $content = $result['content'];

                                $contentStr = "* 请确认新闻记录并更改标注\n* 新闻序号：$num\n* 标题：$title\n* 内容：$content\n———————————————\n* 请输入标注类别：0 无关信息  1 公交爆炸  2 暴恐  3 校园砍杀  q 退出";
                                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                echo $resultStr;

                                $sql = "update user set state = '220',record_id = '$num' where fromUsername = '$fromUsername'";
                                $mysql->runSql($sql);
                            }else{
                                $contentStr = "* 不存在对应该num的已标注新闻记录！\n* 请再次输入需要更改的新闻记录对应num：";
                                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                echo $resultStr;
                                $sql = "update user set state = '0',record_id = '0' where fromUsername = '$fromUsername'";
                                $mysql->runSql($sql)
 
                            }
                            break;
                        case 220:
                            if($keyword == 'q' || $keyword == 'Q'){
                                $contentStr = "* 您选择了取消更改\n";
                                $contentStr .= $main;
                                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                echo $resultStr;

                                $sql = "update user set state = '0',record_id = '0' where fromUsername = '$fromUsername'";
                                $mysql->runSql($sql);

                            }else if( $keyword == '1' || $keyword == '2' || $keyword == '3' || $keyword == '0') {
                                $post_string = '{"force":true,"method":"upsert","resource_id":"'.$newsID.'","records":[{"num":"'.$record_id.'","hit_tag":"'.$keyword.'"}]}';
                                $remote_server = 'http://202.121.178.242/api/3/action/datastore_upsert';
                                $context = array(
                                    'http'=>array(
                                        'method'=>'POST',
                                        'header'=>'Authorization: a6c2ce2d-9e11-4be0-9ffb-ffe4966ed9e2',
                                        'content'=>$post_string)
                                );
                                $stream_context = stream_context_create( $context );
                                $data = json_decode( file_get_contents( $remote_server, FALSE, $stream_context ), true );
                                $contentStr = "* 您已成功更改一条新闻记录！\n".$main;

                                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                echo $resultStr;

                                $sql = "update user set state = '0', record_id = '0' where fromUsername = '$fromUsername'";
                                $mysql->runSql($sql);

                            }else{
                                $contentStr = "* 信息输入有误，请重新更改！\n* 请输入标注类别：0 无关信息  1 公交爆炸  2 暴恐  3 校园砍杀  q 退出";
                                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                                echo $resultStr;
                            }
                            break;

                        case 3:
                            $sql = "update user set state = '0', nickname = '".$keyword."' where fromUsername = '$fromUsername'";
                            $mysql->runSql($sql);
                            $contentStr = "* Hello ".$keyword."\n".$main;
                            $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                            echo $resultStr;
                            break;

                        default:
                            # code...
                            break;
                    }
                    break;

                case 'event':
                    $keyword = trim($postObj->Event);
                    switch ($keyword) {
                        case 'subscribe':
                            $sql = "insert into user values('$fromUsername','0','0','0','0','默默无闻的标注党')";
                            $mysql->runSql($sql);

                            $contentStr = "欢迎关注OmniEye！\n通过OmniEye可以轻松访问Ckan进行记录标注！\n预祝上海交通大学OmniEye团队在开放数据比赛中斩获佳绩！\n$main";
                            $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
                            echo $resultStr;

                            break;

                        case 'unsubscribe':
                            $sql = "delete from user where fromUsername='$fromUsername'";
                            $mysql->runSql($sql);

                            break;

                        default:
                            break;
                    }
                    break;

                case 'image':
                    break;   

                case 'voice':
                    break;

                case 'video':
                    break;  

                case 'location':  
                    break;

                case 'link':
                    break;

                default:
                    break;
            }
            $mysql->closeDb();

        }else {
            
        }
    }
}
?>