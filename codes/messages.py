from flask import render_template, request, flash, session, url_for, redirect, jsonify
from views import *
from flask.views import View

rooms = ''
receiver = ''


class Chatting(View):

    def dispatch_request(self):

        if 'loggedin' in session:
            me = session['id']

            name = Conn.toProfile(me)
            myname = name.fullname

            #
            # chat list = get URL
            #
            inbox = db.session.query(chatrooms).filter(
                chatrooms.c.my_id == me).order_by(desc(chatrooms.c.id)).all()
            urId = []
            for i in inbox:

                # get id from fulnname
                stmt = db.session.query(User).filter(
                    User.fullname == i.user_name).first()
                urId.append(stmt.id)

            #
            # whose sending msg
            #
            checkMsg = db.session.query(chatrooms).filter(
                chatrooms.c.my_id == me).order_by(desc(chatrooms.c.id)).all()
            myMsg = []
            for i in checkMsg:
 
                if i.flag == "1":
                    myMsg.append(1)
                else:
                    myMsg.append(0)


            return render_template('/inbox.html', me=me, myname=myname, inbox=inbox, myMsg=myMsg, urId=urId, msgpage=True)

        return render_template('/login.html')

    def inbox(sendto):

        global rooms, receiver
        a = str(session['id'])
        b = str(sendto) 
        receiver = b

        startchat = Conn.toProfile(b)        

        history = db.session.query(Chat).filter(or_(
            Chat.chatroom == (a + "and" + b), Chat.chatroom == (b + "and" + a))).order_by(asc(Chat.id)).all()

        picbox = db.session.query(chatrooms).filter(or_(
            chatrooms.c.room_id == (a + "and" + b), chatrooms.c.room_id == (b + "and" + a))).all()
         

        if history:
            rooms = history[0].chatroom
        else:
            rooms = (a + "and" + b)

            if rooms == (a+'and'+a) or rooms == (b+'and'+b):
                return redirect(url_for('inboxes')) 
            else:

                aa = Conn.toProfile(a)
                bb = Conn.toProfile(b)
                if aa.role == bb.role:
                    return redirect(url_for('inboxes'))
            
        createTable = Chat(chatroom=rooms, message='Xx_st4rt|r00m_xX')
        db.session.add(createTable)
        db.session.commit()

        return render_template('/chat.html', me=a, picbox=picbox, history=history, rooms=rooms, startchat=startchat ,msgpage=True)

    def message():

        if request.method == "POST":
            try:

                me = session['id']
                username = request.form.get('username')
                message = request.form.get('message') 

                sender = Conn.toProfile(username)
                pic = sender.pic
                  

                # CREATE >> chat
                startchat = Chat(chatroom=rooms, username=username,
                                 message=message, pic=pic, date_time=datetime.now())
                db.session.add(startchat)

                # CLEAR >> sender chatroom (for new message)
                try:
                    del_sender = (delete(chatrooms).where(
                        chatrooms.c.my_id == me, chatrooms.c.room_id == rooms))
                    db.session.execute(del_sender)
                    db.session.commit()
                except:
                    pass

                # RECREATE >> chatroom
                user_sender = Conn.toProfile(me)
                myname = user_sender.fullname
                mypic = user_sender.pic

                user_tosend = Conn.toProfile(receiver)
                urid = user_tosend.id
                urname = user_tosend.fullname
                urpic = user_tosend.pic

                timesent = datetime.now()

                # CREATE >> sender INBOX
                create_inbox = chatrooms.insert().values(my_id=me, user_pic=urpic, user_name=urname,
                                                         room_id=rooms, room_message=message, date_time=timesent, flag=True)
                db.session.execute(create_inbox)

                # UPDATE new message for receiver
                # CLEAR >> receiver chatroom (for new message)
                try:
                    del_receiver = (delete(chatrooms).where(
                        chatrooms.c.my_id == urid, chatrooms.c.room_id == rooms))
                    db.session.execute(del_receiver)
                    db.session.commit()
                except:
                    pass
                    print('failed')

                # CREATE NEW >> receiver chatroom (for new message)
                new_receiver = chatrooms.insert().values(my_id=urid, user_pic=mypic, user_name=myname,
                                                         room_id=rooms, room_message=message, date_time=timesent, flag=False)
                db.session.execute(new_receiver)

                db.session.commit()
                print('commit All PASS')
                dt = datetime.now().strftime('%H:%M u.')

                pusher_client.trigger(
                    rooms, 'new-message', {'username': username, 'message': message, 'datetime': dt, 'pic': pic})

                return jsonify({'result': 'success'})

            except:

                # res = []
                # for i in 0:
                #    if i not in res:
                #        res.append(i)

                return jsonify({'result': 'failure'})
