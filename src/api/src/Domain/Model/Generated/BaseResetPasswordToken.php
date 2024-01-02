<?php
/**
 * This file has been automatically generated by TDBM.
 *
 * DO NOT edit this file, as it might be overwritten.
 * If you need to perform changes, edit the ResetPasswordToken class instead!
 */

declare(strict_types=1);

namespace App\Domain\Model\Generated;

use App\Domain\Model\User;
use TheCodingMachine\TDBM\AbstractTDBMObject;
use TheCodingMachine\TDBM\ResultIterator;
use TheCodingMachine\TDBM\AlterableResultIterator;
use Ramsey\Uuid\Uuid;
use JsonSerializable;
use TheCodingMachine\TDBM\Schema\ForeignKeys;
use TheCodingMachine\GraphQLite\Annotations\Field as GraphqlField;

/**
 * The BaseResetPasswordToken class maps the 'reset_password_tokens' table in
 * database.
 */
abstract class BaseResetPasswordToken extends \TheCodingMachine\TDBM\AbstractTDBMObject implements JsonSerializable
{
    /**
     * @var \TheCodingMachine\TDBM\Schema\ForeignKeys
     */
    private static $foreignKeys = null;

    /**
     * The constructor takes all compulsory arguments.
     *
     * @param \App\Domain\Model\User $user
     * @param string $token
     * @param \DateTimeImmutable $validUntil
     */
    public function __construct(\App\Domain\Model\User $user, string $token, \DateTimeImmutable $validUntil)
    {
        parent::__construct();
        $this->setUser($user);
        $this->setToken($token);
        $this->setValidUntil($validUntil);
        $this->setId(Uuid::uuid1()->toString());
    }

    /**
     * The getter for the "id" column.
     *
     * @return string
     */
    public function getId() : string
    {
        return $this->get('id', 'reset_password_tokens');
    }

    /**
     * The setter for the "id" column.
     *
     * @param string $id
     */
    public function setId(string $id) : void
    {
        $this->set('id', $id, 'reset_password_tokens');
    }

    /**
     * Returns the User object bound to this object via the user_id column.
     */
    public function getUser() : \App\Domain\Model\User
    {
        return $this->getRef('from__user_id__to__table__users__columns__id', 'reset_password_tokens', \App\Domain\Model\User::class, \App\Domain\ResultIterator\UserResultIterator::class);
    }

    /**
     * The setter for the User object bound to this object via the user_id column.
     */
    public function setUser(\App\Domain\Model\User $object) : void
    {
        $this->setRef('from__user_id__to__table__users__columns__id', $object, 'reset_password_tokens', \App\Domain\Model\User::class, \App\Domain\ResultIterator\UserResultIterator::class);
    }

    /**
     * The getter for the "token" column.
     *
     * @return string
     */
    public function getToken() : string
    {
        return $this->get('token', 'reset_password_tokens');
    }

    /**
     * The setter for the "token" column.
     *
     * @param string $token
     */
    public function setToken(string $token) : void
    {
        $this->set('token', $token, 'reset_password_tokens');
    }

    /**
     * The getter for the "valid_until" column.
     *
     * @return \DateTimeImmutable
     */
    public function getValidUntil() : \DateTimeImmutable
    {
        return $this->get('valid_until', 'reset_password_tokens');
    }

    /**
     * The setter for the "valid_until" column.
     *
     * @param \DateTimeImmutable $validUntil
     */
    public function setValidUntil(\DateTimeImmutable $validUntil) : void
    {
        $this->set('valid_until', $validUntil, 'reset_password_tokens');
    }

    /**
     * Internal method used to retrieve the list of foreign keys attached to this bean.
     */
    protected static function getForeignKeys(string $tableName) : \TheCodingMachine\TDBM\Schema\ForeignKeys
    {
        if ($tableName === 'reset_password_tokens') {
            if (self::$foreignKeys === null) {
                self::$foreignKeys = new ForeignKeys([
                    'from__user_id__to__table__users__columns__id' => [
                        'foreignTable' => 'users',
                        'localColumns' => [
                            'user_id'
                        ],
                        'foreignColumns' => [
                            'id'
                        ]
                    ]
                ]);
            }
            return self::$foreignKeys;
        }
        return parent::getForeignKeys($tableName);
    }

    /**
     * Serializes the object for JSON encoding.
     *
     * @param bool $stopRecursion Parameter used internally by TDBM to stop embedded
     * objects from embedding other objects.
     * @return array
     */
    public function jsonSerialize(bool $stopRecursion = false)
    {
        $array = [];
        $array['id'] = $this->getId();
        if ($stopRecursion) {
            $array['user'] = ['id' => $this->getUser()->getId()];
        } else {
            $array['user'] = $this->getUser()->jsonSerialize(true);
        }
        $array['token'] = $this->getToken();
        $array['validUntil'] = $this->getValidUntil()->format('c');
        return $array;
    }

    /**
     * Returns an array of used tables by this bean (from parent to child
     * relationship).
     *
     * @return string[]
     */
    public function getUsedTables() : array
    {
        return [ 'reset_password_tokens' ];
    }

    /**
     * Method called when the bean is removed from database.
     */
    public function onDelete() : void
    {
        parent::onDelete();
        $this->setRef('from__user_id__to__table__users__columns__id', null, 'reset_password_tokens', \App\Domain\Model\User::class, \App\Domain\ResultIterator\UserResultIterator::class);
    }

    public function __clone()
    {
        parent::__clone();
        $this->setId(Uuid::uuid1()->toString());
    }
}
